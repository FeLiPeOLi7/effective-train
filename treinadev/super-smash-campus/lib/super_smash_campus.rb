class SuperSmashCampus
  attr_reader :combatants, :events

  def initialize(combatants, events)
    @combatants = combatants
    @events = events
  end

  def readEvents(events)
    fights = events.split("\n")
    fights_results = []
  
    fights.each do |fight|
      if(fight =~ /Luta: (.+) vs (.+), (.+) vence/)
        fighter_left = $1
        fighter_right = $2
        winner = $3
        result = {:fighter_left => fighter_left, :fighter_right => fighter_right, :winner => winner, :fight => 1}
      elsif(fight =~ /Treino: (.+), (.+)/)
        fighter = $1
        xp = $2.scan(/../).first
        result = {:fighter => fighter, :exp => xp.to_i, :fight => 0}
      end
     fights_results.push(result)
    end
    return fights_results
  end

  def adventure!
    battles = readEvents(events)

    battles.each do |battle|
      combatants.each do |winner|
        if(battle[:fight] == 1)
          combatants.each do |loser|
            if(winner.name == battle[:winner])
              if((loser.name == battle[:fighter_left] || loser.name == battle[:fighter_right]) && loser.name != battle[:winner])
                winner_previous_level = winner.level
                winner.add_victory_exp(loser.level)
                loser.add_defeat_exp(winner_previous_level)
              end
            end
          end
        else
          if(winner.name == battle[:fighter])
            winner.exp += battle[:exp]
          end
        end
      end
    end

  end
end