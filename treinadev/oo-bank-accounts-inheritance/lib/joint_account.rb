class JointAccount < BankAccount 
    attr_accessor :super_account

    def initialize(name:, number:, super_account:)
        super(name: name, number: number, balance: super_account.balance)
        @super_account = super_account
    end

    def debit(value)
        super(value)

        super_account.debit(value)
    end
    
    def deposit(value)
        super(value)

        super_account.deposit(value)
    end 
end
