"""
Generate Predictions
-------------------------------------------

This script provides functionalities to generate predictions using a machine learning model,
along with tokenization and detokenization processes that convert strings to a list of tokens
and back. The tokenization and detokenization rely on a predefined set of tokens
specified in a file.
"""

import torch
import torch.nn.functional as F

from src.tokenizer.tokenizer import tokenize_data
from src.tokenizer.detokenizer import detokenize_data


def convert_string_to_list(tokenized_string):
    """
    Converts a string of integers into a list of integers. If the input string is empty,
    it returns a list containing the BOS token (75).

    Parameters:
    - `tokenized_string` (str): A string of space-separated integers representing tokenized data.

    Returns:
    - `List[int]`: A list of integers parsed from the input string.
    """

    token_list = list(map(int, tokenized_string.split()))
    if len(token_list) == 0:
        token_list = [75]
    return token_list


def convert_list_to_string(token_list):
    """
    Converts a list of integers into a string of integers separated by spaces.

    Parameters:
    - `token_list` (List[int]): A list of integers to be converted into a tokenized string.

    Returns:
    - `str`: A space-separated string of integers.
    """

    return " ".join(map(str, token_list))


def model_predict(model, input_ids, num_tokens_to_generate, temperature=1.0):
    """
    Model Predict
    -------------

    Generates predictions using a pretrained model given a batch of tokenized input IDs.

    Parameters:
    - `model` (torch.nn.Module): The pre-trained language model for generating predictions.
    - `input_ids` (torch.Tensor): A tensor of tokenized input IDs.
    - `num_tokens_to_generate` (int): The number of tokens to generate.
    - `temperature` (float): The temperature setting for the generation process. Default is 1.0.

    Returns:
    - `torch.Tensor`: The model's prediction as a tensor of output IDs.

    Example:
        >>> model = YourModel()  # replace with your actual model
        >>> input_ids = torch.tensor([[12, 23, 34, 45]])
        >>> prediction = model_predict(model, input_ids, num_tokens_to_generate=10)
        >>> print(prediction)
    """

    with torch.no_grad():
        prediction = model.generate(
            input_ids,
            max_length=input_ids.shape[1] + num_tokens_to_generate,
            num_return_sequences=1,
            eos_token_id=74,  # If token 74 (gameSeparator) is produced, stop generating
            pad_token_id=0,
            temperature=temperature,
            do_sample=True,
        )
    return prediction


def generate_prediction(
    input, num_tokens_to_generate, model, notation, temperature=1.0, seed=None
):
    """
    Generate Prediction
    -------------------

    Generates a prediction for an input string using the model. It tokenizing the input and detokenizing the output.

    Parameters:
    - `input` (str): The input string for which to generate a prediction.
    - `num_tokens_to_generate` (int): The number of tokens to generate in the prediction.
    - `model` (torch.nn.Module): The pre-trained language model used for generating predictions.
    - `notation` (str): The notation for which the token mappings are defined.
    - `temperature` (float): The temperature setting for the generation process. Default is 1.0.
    - `seed` (Optional[int]): A seed for the random number generator. Default is None.

    Returns:
    - Tuple[str, str, str]: A tuple containing the detokenized output, predicted token string, and original tokenized string.

    Example:
        >>> input_string = "Pd2d4 Pe7e5"
        >>> output_text, token_string, original_token_string = generate_prediction(
                input_string, num_tokens_to_generate=3, model=model, notation='xLANplus'
            )
        >>> print(output_text)
    """
    original_device = next(model.parameters()).device
    model.to("cuda" if torch.cuda.is_available() else "cpu")
    device = next(model.parameters()).device

    if seed is not None:
        torch.manual_seed(seed)

    tokenized_string = tokenize_data(input_data=input, notation=notation)
    token_list = convert_string_to_list(tokenized_string)

    input_ids = torch.tensor([token_list])
    input_ids = input_ids.to(device)

    prediction = model_predict(model, input_ids, num_tokens_to_generate, temperature)

    predicted_token_list = prediction[0].cpu().numpy().tolist()
    predicted_token_string = convert_list_to_string(predicted_token_list)
    detokenized_output = detokenize_data(
        tokenized_data=predicted_token_string, notation=notation
    )

    model.to(original_device)

    return detokenized_output, predicted_token_string, tokenized_string


def generate_batch_predictions(
    inputs,
    num_tokens_to_generate,
    model,
    notation,
    temperature=1.0,
    seed=None,
    max_batch_size=30,
    left_side_padding=False,
):
    """
    Generate Batch Predictions
    --------------------------

    Generates predictions for a batch of input strings using the model. It tokenizing the input
    and detokenizing the output.

    Parameters:
    - `inputs` (List[str]): A list of input strings for which to generate predictions.
    - `num_tokens_to_generate` (int): The number of tokens to generate for each prediction.
    - `model` (torch.nn.Module): The pre-trained language model used for generating predictions.
    - `notation` (str): The notation for which the token mappings are defined.
    - `temperature` (float): The temperature setting for the generation process. Default is 1.0.
    - `seed` (Optional[int]): A seed for the random number generator. Default is None.

    Returns:
    - Tuple[List[str], List[str], List[str]]: A tuple containing lists of the detokenized outputs, predicted token strings, and original tokenized strings.

    Example:
        >>> inputs = ["First input string", "Second input string"]
        >>> outputs, token_strings, original_token_strings = generate_batch_predictions(
                inputs, num_tokens_to_generate=10, model=model, notation='xLANplus'
            )
        >>> print(outputs)
    """
    original_device = next(model.parameters()).device
    model.to("cuda" if torch.cuda.is_available() else "cpu")
    device = next(model.parameters()).device

    detokenized_outputs = []
    predicted_token_strings = []
    tokenized_strings = []

    input_batches = [
        inputs[i : i + max_batch_size] for i in range(0, len(inputs), max_batch_size)
    ]

    for batch in input_batches:
        if seed is not None:
            torch.manual_seed(seed)

        tokenized_batch_strings = [
            tokenize_data(input_data=input, notation=notation) for input in batch
        ]
        token_lists = [
            convert_string_to_list(tokenized_string)
            for tokenized_string in tokenized_batch_strings
        ]

        # Pad token lists to the same length if they vary in length
        max_length = max(map(len, token_lists))

        if left_side_padding:
            padded_token_lists = [
                [0] * (max_length - len(token_list)) + token_list
                for token_list in token_lists
            ]
        else:
            padded_token_lists = [
                token_list + [0] * (max_length - len(token_list))
                for token_list in token_lists
            ]
        input_ids = torch.tensor(padded_token_lists)
        input_ids = input_ids.to(device)

        predictions = model_predict(
            model, input_ids, num_tokens_to_generate, temperature
        )

        predictions = predictions.cpu()

        # Decoding predictions with detokenizer
        predicted_token_lists = [
            single_prediction.numpy().tolist() for single_prediction in predictions
        ]
        predicted_batch_token_strings = [
            convert_list_to_string(token_list) for token_list in predicted_token_lists
        ]
        detokenized_batch_outputs = [
            detokenize_data(tokenized_data=token_string, notation=notation)
            for token_string in predicted_batch_token_strings
        ]
        detokenized_outputs.extend(detokenized_batch_outputs)
        predicted_token_strings.extend(predicted_batch_token_strings)
        tokenized_strings.extend(tokenized_batch_strings)

        if seed is not None:
            seed += 1

    model.to(original_device)

    return (
        detokenized_outputs,
        predicted_token_strings,
        tokenized_strings,
    )


def generate_beam(input, model, notation, num_tokens_to_generate=3, beam_size=10):
    """
    Generate Beam
    -------------

    Generates predictions using a beam search approach. It tokenizes the input and detokenizes the output.
    Beam search is a heuristic search algorithm that explores a graph by expanding the most promising node.
    It returns a list of top predictions for each input sequence.
    It has a runtime complexity of O(b^d), where b is the beam size and d is the num_tokens_to_generate.

    Parameters:
    - `input` (str): The input string for which to generate predictions.
    - `model` (torch.nn.Module): The pre-trained language model used for generating predictions.
    - `notation` (str): The notation for which the token mappings are defined.
    - `num_tokens_to_generate` (int): The length of the sequence to generate. Default is 3.
    - `beam_size` (int): The number of top sequences to keep after each generation step. Default is 10.

    Returns:
    - List[Tuple[str, float]]: A list of tuples containing the generated sequences and their respective probabilities.

    Example:
        >>> input_string = "The quick brown fox"
        >>> sequences = generate_beam(input_string, model, 'xLANplus', sequence_length=5, beam_size=5)
        >>> print(sequences)
    """

    beam = []
    start_prob = 1.0

    device = next(model.parameters()).device

    def predict_next_tokens(input_tokens, cur_sequence, cur_prob, depth):
        if depth == num_tokens_to_generate:
            # If sequence is complete, store it and return
            beam.append((cur_sequence, cur_prob))
            return

        tokenized_string = tokenize_data(input_data=input_tokens, notation=notation)
        token_list = convert_string_to_list(tokenized_string)

        input_ids = torch.tensor([token_list])
        input_ids = input_ids.to(device)
        with torch.no_grad():
            output = model(input_ids)
            logits = output.logits

        # Getting probabilities using softmax
        probabilities = F.softmax(logits[0, -1, :], dim=0)

        top_probs, top_indices = torch.topk(probabilities, beam_size)

        # Iterate over top predictions
        for i, move_prob in zip(top_indices, top_probs):
            token = convert_list_to_string([i.item()])
            # Append predicted token to current sequence
            new_sequence = cur_sequence + [
                detokenize_data(tokenized_data=token, notation=notation)
            ]
            new_prob = cur_prob * move_prob.item()  # Multiply probabilities
            # Recursively predict next tokens
            predict_next_tokens(
                input_tokens + detokenize_data(token, notation=notation),
                new_sequence,
                new_prob,
                depth + 1,
            )

    # Start the recursive prediction
    predict_next_tokens(input, [], start_prob, 0)
    sorted_beam = sorted(beam, key=lambda x: x[1], reverse=True)

    return sorted_beam[:beam_size]
