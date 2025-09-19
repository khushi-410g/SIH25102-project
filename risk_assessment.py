# Rule-Based Risk Identification Logic in Python

def attendance_risk(attendance_percentage, threshold=75):
    """
    Evaluate risk based on attendance.
    :param attendance_percentage: float, attendance rate in percentage
    :param threshold: int, minimum acceptable attendance percentage
    :return: str, 'low' or 'high' risk
    """
    if attendance_percentage < threshold:
        return 'high'
    return 'low'


def test_score_risk(current_score, previous_score=None, low_score_threshold=50, decline_threshold=10):
    """
    Evaluate risk based on test scores.
    :param current_score: int, current test score
    :param previous_score: int or None, previous test score to check decline
    :param low_score_threshold: int, score below which risk is high
    :param decline_threshold: int, minimum decline in score to consider risk
    :return: str, 'low' or 'high' risk
    """
    if current_score < low_score_threshold:
        return 'high'
    if previous_score is not None and (previous_score - current_score) >= decline_threshold:
        return 'high'
    return 'low'


def fee_payment_risk(fee_paid):
    """
    Evaluate risk based on fee payment status.
    :param fee_paid: bool, True if fee is paid, False otherwise
    :return: str, 'low' or 'high' risk
    """
    return 'low' if fee_paid else 'high'


def overall_risk(attendance_pct, current_score, previous_score, fee_paid):
    """
    Combine multiple risk factors to assign overall risk level.
    :param attendance_pct: float, attendance percentage
    :param current_score: int, current test score
    :param previous_score: int or None, previous test score
    :param fee_paid: bool, fee payment status
    :return: str, overall risk level ('low', 'medium', 'high')
    """
    risks = [
        attendance_risk(attendance_pct),
        test_score_risk(current_score, previous_score),
        fee_payment_risk(fee_paid)
    ]

    high_risk_count = risks.count('high')

    if high_risk_count == 0:
        return 'low'
    elif high_risk_count == 1:
        return 'medium'
    else:
        return 'high'


# Example usage
if __name__ == "__main__":
    attendance = 70  # in percentage
    current_test_score = 45
    previous_test_score = 60
    fee_paid_status = False

    risk_level = overall_risk(attendance, current_test_score, previous_test_score, fee_paid_status)
    print(f"Overall Risk Level: {risk_level}")
