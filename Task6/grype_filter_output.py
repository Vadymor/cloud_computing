import os
import pandas as pd


def execute_grype_command() -> str:
    grype_output_stream = os.popen("grype docker:ghcr.io/mlflow/mlflow:v2.3.0")

    grype_output = grype_output_stream.read()

    return grype_output


def get_slices(header_line: str) -> list[int]:
    slices = [0]

    for i in range(len(header_line) - 1):
        if header_line[i] == ' ' and header_line[i + 1] != ' ':
            slices.append(i + 1)

    slices.append(len(header_line) + 1)

    return slices


def transform_body(body, slices):
    data = []

    for i in body:

        tmp_line = []
        for sl in range(len(slices) - 1):
            tmp_line.append(i[slices[sl]: slices[sl + 1]].strip())

        data.append(tmp_line)

    return data


def main():

    # execute grype and store results in string
    output: str = execute_grype_command()

    # retrieve from output header line and body
    header = output.split('\n')[0]
    body = output.split('\n')[1:]

    # get columns slices
    slices_idx = get_slices(header)

    # transform data into list of lists
    transformed_data = transform_body(body, slices_idx)

    # put data into DataFrame
    df = pd.DataFrame(transformed_data, columns=['NAME', 'INSTALLED', 'FIXED-IN', 'TYPE', 'VULNERABILITY', 'SEVERITY'])

    # filter CVEs for fixed HIGH and CRITICAL vulnerabilities.
    filtered = df.loc[(df['FIXED-IN'] != "(won't fix)") &
                      (df['FIXED-IN'] != '') &
                      (df['SEVERITY'].isin(['High', 'Critical'])), :]

    print(filtered.to_string())


if __name__ == '__main__':
    main()
