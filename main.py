import json
from gpt4all import GPT4All


class DeliberationPipeline:
    def __init__(self, config_path):
        with open(config_path, "r") as f:
            self.config = json.load(f)

        self.model = GPT4All(self.config["model"]["name"],
        model_path="",allow_download=False,n_threads=8,device="cpu")
        self.roles = self.config["roles"]
        self.max_tokens = self.config["model"]["max_tokens"]
        self.max_rounds = self.config["pipeline"]["max_rounds"]
        self.show = self.config["pipeline"]["show_discourse"]

    def run_step(self, role_name, input_text):
        role = self.roles[role_name]

        prompt = (
            f"[SYSTEM]\n{role['system']}\n[/SYSTEM]\n\n"
            f"{input_text}\n\nOutput:"
        )

        with self.model.chat_session():
            return self.model.generate(
                prompt,
                max_tokens=self.max_tokens,
                temp=role["temperature"]
            )

    def log(self, title, content):
        if self.show:
            print(f"=== {title.upper()} ===\n{content}\n")

    def run(self, question):
        print(f"\nUSER QUESTION:\n{question}\n")

        draft = self.run_step("writer", question)
        self.log("writer", draft)

        for i in range(self.max_rounds):
            critique = self.run_step(
                "critic",
                f"Question:\n{question}\n\nDraft:\n{draft}"
            )
            self.log("critic", critique)

            improved = self.run_step(
                "refiner",
                f"Question:\n{question}\n\nDraft:\n{draft}\n\nCritique:\n{critique}"
            )
            self.log("refiner", improved)

            verdict = self.run_step(
                "judge",
                f"Question:\n{question}\n\nAnswer:\n{improved}"
            )
            self.log("judge", verdict)

            draft = improved

            if "PASS" in verdict.upper():
                print("✅ Accepted by judge\n")
                break

        print("=== FINAL ANSWER ===\n", draft)
        return draft


if __name__ == "__main__":
    pipeline = DeliberationPipeline("config.json")
    question = input("Ask a question: ")
    pipeline.run(question)