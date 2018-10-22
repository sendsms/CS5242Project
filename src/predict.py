import argparse
import os
import pickle
import csv
import logging
import keras

from collections import defaultdict

from keras.models import load_model

from settings import TESTING_EXAMPLES_FOLDER
from predict_generator import PredictGenerator
from settings import PREDICT_EXAMPLES_FOLDER, RESULTS_FOLDER
from train_cnn import f1


def calculate_success_rate(matching_list: list):
    """
    Compute the final success rate using a matching list

    :param matching_list:
    :return: a number in [0,1] representing the final success rate
    """
    success_count = 0
    failure_count = 0
    for item in matching_list:
        protein_indice = item[0]
        ligend_indices = item[1:]
        if protein_indice in ligend_indices:
            success_count += 1
        else:
            failure_count += 1
    return success_count / (success_count + failure_count)


def predict(serialized_model_path, evaluation=True):
    """
    Predict the results with a model.

    :param serialized_model_path:
    :param evaluation:
    :return:
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(os.path.join(RESULTS_FOLDER, 'prediction.log'))
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    id = serialized_model_path.split(os.sep)[-2]
    job_folder = os.path.join(RESULTS_FOLDER, id)
    matching_file_name = os.path.join(job_folder, f"{id}_matching.pkl")
    result_file_name = os.path.join(job_folder, f"{id}_result.txt")

    if evaluation:
        predict_folder = TESTING_EXAMPLES_FOLDER
    else:
        predict_folder = PREDICT_EXAMPLES_FOLDER
    logger.debug(f'Using example folder: {predict_folder}.')

    # Load pre-trained good model
    my_model = load_model(serialized_model_path, custom_objects={'f1': f1})
    logger.debug(f'Model loaded. Summary: ')
    keras.utils.print_summary(my_model, print_fn=logger.debug)

    matching = defaultdict(list)

    predict_examples_generator = PredictGenerator(predict_folder)
    for pro, lig, cube in predict_examples_generator:
        y_predict = my_model.predict(cube)

        matching[pro].append((y_predict[0][0], lig))

    with open(matching_file_name, 'wb') as f:
        pickle.dump(matching, f)
        logger.debug(f'Matching pickle file saved {matching_file_name}')

    matching_list = []

    with open(os.path.join(RESULTS_FOLDER, 'result.txt'), 'w') as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow('pro_id  lig1_id lig2_id lig3_id lig4_id lig5_id lig6_id lig7_id lig8_id lig9_id lig10_id')
        for pro, ligands_score in sorted(matching.items()):
            top_10 = sorted(ligands_score, reverse=True)[:10]
            top_10_ligands = list(map(lambda x: x[1], top_10))
            row = [pro, *top_10_ligands]
            matching_list.append(row)
            csvwriter.writerow(" ".join(row))
        logger.debug(f'Result file saved {result_file_name}')

    success_rate = calculate_success_rate(matching_list)
    logger.debug(f'Success rate for model {id} is : {success_rate}')


if __name__ == "__main__":
    # Parsing sysargv arguments
    parser = argparse.ArgumentParser(description='Evaluate a model using a serialized version of it.')

    parser.add_argument('--model_path', metavar='model_path',
                        type=str, required=True,
                        help=f'where the serialized file of the model (.h5) is.')

    parser.add_argument('--evaluation', metavar='evaluation',
                        type=bool, default=True,
                        help='if true: action on test data from training set')

    args = parser.parse_args()

    print("Argument parsed : ", args)

    predict(serialized_model_path=args.model_path,
            evaluation=args.evaluation)
