import re
from typing import Any, DefaultDict, Dict

import WDL as wdl


class MarkDownDoc:
    def __init__(self, title: str) -> None:
        self.title = f"# {title}"
        self.front_matter = ""
        self.inputs = "\n## Inputs"
        self.outputs = "\n## Outputs"
        self.todo = "\n## To Do"

    def generate_frontmatter(self, source_text: str) -> None:
        comments = re.findall("^##.*", source_text, re.MULTILINE)
        for comment in comments:
            self.front_matter += comment[3:] + "\n"

    def generate_inputs(
        self,
        inputs: DefaultDict[str, DefaultDict[str, wdl.Env.Binding]],
        parameter_metadata: Dict[str, Any],
    ) -> None:
        if inputs["required"].items():
            self.inputs += "\n#### Required"
        for name, value in inputs["required"].items():
            self.inputs += f"\n  * `{name}` ({value.type}, **required**)"
            description = parameter_metadata.get(value.name)
            if description:
                self.inputs += ": {}".format(description)

        if inputs["optional"].items():
            self.inputs += "\n#### Optional"
        for name, value in inputs["optional"].items():
            self.inputs += f"\n  * `{name}` ({value.type})"
            description = parameter_metadata.get(value.name)
            if description:
                self.inputs += ": {}".format(description)

        if inputs["default"].items():
            self.inputs += "\n#### Defaults"
        for name, value in inputs["default"].items():
            self.inputs += f"\n  * `{name}` ({value.type}, default={value.expr})"
            description = parameter_metadata.get(value.name)
            if description:
                self.inputs += ": {}".format(description)

        if self.inputs == "## Inputs":
            self.inputs += "\nNone"

    def generate_outputs(self, outputs: wdl.Env.Bindings) -> None:
        for output in outputs:
            self.outputs += f"\n  * `{output.name}` ({output.value})"

        if self.outputs == "## Outputs":
            self.outputs += "\nNone"