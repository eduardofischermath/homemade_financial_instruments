public class InstallmentLoan {

    // Determines time unit of calculations
    // Only this possibility for now [formulas are the same]
    String timeUnit = "month";

    // Determines whether non-integer number of installments are allowed, and
    // whether nonpositive values for the 4 key variables are allowed
    boolean numbersMakeSense = false;

    public static void main(String[] args) {

    }

    private float getOutstandingBalanceFromThreeOthers(float installment, float nInstallments, float interestRate) {

    }

    private float getInstallmentFromThreeOthers(float outstandingBalance, float nInstallments, float interestRate) {

    }

    private float getNInstallmentsFromThreeOthers(float outstandingBalance, float installment, float interestRate) {

    }

    private float getInterestRateFromThreeOthers(float outstandingBalance, float installment, float nInstallments) {

    }

}
