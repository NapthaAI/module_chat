#!/usr/bin/env python

from simple_chat_agent.schemas import InputSchema
from simple_chat_agent.utils import get_logger
from litellm import completion
import yaml

logger = get_logger(__name__)

def run(inputs: InputSchema, *args, **kwargs):
    logger.info(f"Running with inputs {inputs.prompt}")
    cfg = kwargs["cfg"]
    logger.info(f"cfg: {cfg}")

    if inputs.llm_backend == "ollama":
        prompt = inputs.prompt
        messages = [
            {"role": "system", "content": cfg["inputs"]["system_message"]},
            {"role": "user", "content": prompt},
        ]
        response = completion(
            model=cfg["models"]["ollama"]["model"],
            messages=messages,
            temperature=cfg["models"]["ollama"]["temperature"],
            max_tokens=cfg["models"]["ollama"]["max_tokens"],
            api_base=cfg["models"]["ollama"]["api_base"],
        )

        response = response.choices[0].message["content"]
        logger.info(f"Response: {response}")

    elif inputs.llm_backend == "vllm":
        messages = [
            {"role": "system", "content": cfg["inputs"]["system_message"]},
            {"role": "user", "content": inputs.prompt}
        ]
        response = completion(
            model=cfg["models"]["vllm"]["model"],
            messages=messages,
            api_base=cfg["models"]["vllm"]["api_base"],
            api_key = "EMPTY",
            temperature=cfg["models"]["vllm"]["temperature"],
            max_tokens=cfg["models"]["vllm"]["max_tokens"],
        )

        response = response.choices[0].message.content
        logger.info(f"Response: {response}")

    return response

if __name__ == "__main__":

    cfg_path = f"simple_chat_agent/component.yaml"
    with open(cfg_path, "r") as file:
        cfg = yaml.load(file, Loader=yaml.FullLoader)

    inputs = InputSchema(
        prompt='tell me a joke',
    )
    response = run(inputs, cfg)


