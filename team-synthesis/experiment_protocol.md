# Experiment Protocol

## Experimental Unit
One frozen HumanEval problem.

## Conditions
1. Human baseline
2. ChatGPT
3. Gemini

## Freeze Before Pilot/Full Run
- Dataset/version and 30 selected problem IDs
- Java/JUnit harness
- Task-category taxonomy
- Prompt version
- Model identifiers and generation settings
- Compile/run timeout
- Repair policy
- Result schema

## AI Procedure
For each problem and each model:
1. Load frozen problem statement/signature.
2. Send the frozen structured prompt.
3. Save the raw response verbatim.
4. Extract JUnit code without manual editing.
5. Compile.
6. If compilation fails, save compiler feedback and perform exactly one repair request.
7. Compile the repaired output once.
8. If compilation succeeds, execute tests.
9. Log every outcome, including empty/invalid output.

## Prohibited
- Manual repair of generated tests.
- More than one repair round.
- Per-problem prompt tuning.
- Dropping failed outputs.
- Retrying until a preferred answer appears.

## Primary Outcome
```text
combined_success = 1 if the generated JUnit suite compiles and executes successfully
combined_success = 0 otherwise
```

## Secondary Outcomes
- compile_success
- execution_success
- repair_needed
- repair_success
- failure_stage
- task_category

## Pilot
Run only 5–10 problems to validate harness, schema, prompt and operational definitions.

## Full Experiment
Run 30 problems only after the protocol is frozen and pilot amendments are recorded.
