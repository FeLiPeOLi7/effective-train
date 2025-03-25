class BankAccount
  attr_reader :balance, :name, :number

  def initialize(name:, number:, balance: 0)
    @name = name
    @number = number
    @balance = balance
  end

  def debit(debit)
    if(@balance - debit >= 0)
      @balance = @balance - debit
    else
      return "Saldo insuficiente."
    end
  end

  def deposit(deposit)
    @balance = @balance + deposit
  end
end
