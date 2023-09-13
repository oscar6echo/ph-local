import re
from pathlib import Path


class Generate:
    """"""

    def __init__(self, tag="mytag", port="92"):
        """"""

        self.tag = tag
        self.port = int(port)

        msg = "port must be between 91 and 99 incl."
        assert 92 <= port <= 99, msg

        self.f_repo = Path(__file__).parent.parent.resolve()
        self.f_compose_ref = self.f_repo / "compose"
        self.f_compose_instance = self.f_repo / f"compose-{self.tag}-{self.port}"

        self.path_in = self.f_compose_ref / "docker-compose.yml"
        self.path_out = self.f_compose_instance / "docker-compose.yml"

        self.path_run_up = self.f_compose_instance / "run-up.sh"
        self.path_run_down = self.f_compose_instance / "run-down.sh"

    def build(self):
        """"""
        txt_in = self.path_in.read_text()
        dic = {
            "mytag": self.tag,
            "91": str(self.port),
        }
        txt_out = Generate.multiple_replace(txt_in, dic)

        self.path_out.parent.mkdir(parents=True, exist_ok=True)
        self.path_out.write_text(txt_out)

        txt_shebang = "#! /bin/bash\n\n"

        txt = f"docker compose --profile {self.tag} up"
        self.path_run_up.write_text(txt_shebang + txt)

        txt = f"docker compose --profile {self.tag} down"
        self.path_run_down.write_text(txt_shebang + txt)

        print(f"created")
        print(f"instance:               {self.path_out.name}")
        print(f"docker-compose.yml:     {self.path_out}")
        print(f"run-up.sh:              {self.path_run_up}")
        print(f"run-down.sh:            {self.path_run_down}")

    def multiple_replace(txt, dic):
        """"""
        if len(dic) == 0:
            return txt

        # Create a regex from the dict keys
        regex = re.compile("(%s)" % "|".join(map(re.escape, dic.keys())))

        # For each match, lookup corresponding value in dict
        return regex.sub(lambda mo: dic[mo.string[mo.start() : mo.end()]], txt)


tag = "olivier"
port = 92

c = Generate(tag, port)
c.build()

print("END")
