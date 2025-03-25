class Combatant
  attr_accessor :exp
  attr_reader :name, :level

  def initialize(name, exp)
    @name = name
    @exp = exp
    @level = (exp/10).round
  end

  def add_victory_exp(level)
    exp_difference = (level - @level)*5
    if(exp_difference < -100)
      exp_difference = -100
    end

    @exp += exp_difference
    @exp += 100

    @level = (@exp/10).round
  end

  def add_defeat_exp(level)
    exp_difference = (level - @level)*5
    if(exp_difference < -50)
      exp_difference = -50
    end
    @exp += exp_difference
    @exp += 50

    @level = (@exp/10).round
  end

  def exp=(xp)
    @exp = xp
    @level = (@exp/10).round
  end
end