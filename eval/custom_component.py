from langflow.custom import Component
from langflow.io import StrInput, DataFrameInput, Output
from langflow.schema import DataFrame, Data
from openevals.llm import create_llm_as_judge
from openevals.prompts import CORRECTNESS_PROMPT

class CorrectnessEvaluator(Component):
    display_name = "Correctness Evaluator"
    description = "Evaluates the correctness of outputs using OpenAI's LLM."
    icon = "check-circle"
    name = "CorrectnessEvaluator"

    inputs = [
        DataFrameInput(
            name="dataframe",
            display_name="DataFrame",
            info="DataFrame containing inputs, outputs, and reference outputs."
        ),
        StrInput(
            name="api_key",
            display_name="OpenAI API Key",
            info="API key for accessing OpenAI services."
        ),
        StrInput(
            name="input_column",
            display_name="Input Column",
            info="Column name for inputs in the DataFrame."
        ),
        StrInput(
            name="output_column",
            display_name="Output Column",
            info="Column name for outputs in the DataFrame."
        ),
        StrInput(
            name="reference_output_column",
            display_name="Reference Output Column",
            info="Column name for reference outputs in the DataFrame."
        )
    ]

    outputs = [
        Output(
            name="evaluation_results",
            display_name="Evaluation Results",
            method="evaluate_correctness"
        )
    ]

    def evaluate_correctness(self) -> DataFrame:
        import os
        os.environ["OPENAI_API_KEY"] = self.api_key

        correctness_evaluator = create_llm_as_judge(
            prompt=CORRECTNESS_PROMPT,
            feedback_key="correctness",
            model="openai:o3-mini",
        )

        results = []
        for _, row in self.dataframe.iterrows():
            inputs = row[self.input_column]
            outputs = row[self.output_column]
            reference_outputs = row[self.reference_output_column]

            eval_result = correctness_evaluator(
                inputs=inputs,
                outputs=outputs,
                reference_outputs=reference_outputs
            )
            results.append(eval_result)

        self.status = f"Evaluated correctness for {len(results)} rows."
        return DataFrame(results)