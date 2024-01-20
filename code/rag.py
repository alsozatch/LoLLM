import dspy
from dspy import evaluate
from dspy import teleprompt

class CoT(dspy.Module):
    def __init__(self):
        super().__init__()

        self.generate_answer = dspy.ChainOfThought('message -> response')

    def forward(self, message):
        return self.generate_answer(message=message)

def main():
    mistral = dspy.HFModel(model="../models/Mistral-7B-v0.1-GPTQ")
    colbertv2 = dspy.ColBERTv2(url='http://20.102.90.50:2017/wiki17_abstracts')

    dspy.settings.configure(rm=colbertv2, lm=mistral)

    teemo_train = [("you suck teemo", "Never underestimate the power of the Scout's code."),
                   ("invade bot", "Yes, sir!"),
                   ("need baron visin", "I'll scout ahead!")]
    
    teemo_train = [dspy.Example(message=message, response=response).with_inputs('message') for message, response in teemo_train]

    metric_EM = evaluate.answer_exact_match

    teleprompter = teleprompt.BootstrapFewShot(metric=metric_EM, max_bootstrapped_demos=2)
    cot_compiled = teleprompter.compile(CoT(), trainset=teemo_train)

    print(cot_compiled("give up teemo"))

    print(mistral.inspect_history(n=1))

if __name__ == '__main__':
    main()