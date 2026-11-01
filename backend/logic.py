
def run_solution(user_input):
    """
    Main function for solving the hackathon problem.

    Args:
        user_input: Data received from the frontend.

    Returns:
        A dictionary containing the result.
    """

    if not user_input or not user_input.strip():
        return {
            "success": False,
            "result": "Please enter some input."
        }

    # TODO: Add your hackathon problem-solving logic here.
    result = f"You entered: {user_input}"

    return {
        "success": True,
        "result": result
    }

