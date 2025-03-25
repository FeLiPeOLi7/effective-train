class TurnBasedGame
  attr_reader :characters, :gamelog, :output

  def initialize(characters, gamelog)
    @characters = characters
    @gamelog = gamelog.split("\n")
    @output = <<~OUTPUT.chomp
    OUTPUT
  end

  def play

    gamelog.each do |turn|
      characters.each do |agent|
        characters.each do |object|
          if(turn =~ /(.+) ataca (.+)/)
            if(agent.name == $1 && object.name == $2)
              life = object.life
              real_strength = agent.attack(object)
              if(life > 0)
                if(object.life > 0)
                  @output += "#{agent.name} => #{object.name}: #{life} - #{real_strength} => #{object.life}\n"
                else
                  @output += "#{agent.name} => #{object.name}: #{life} - #{real_strength} => nocauteado\n"
                end
              else
                @output += "#{agent.name} => #{object.name}: nocauteado\n"
              end
            end
          elsif(turn =~ /(.+) cura (.+)/)
            if(agent.name == $1 && object.name == $2)
              life = object.life
              healed = agent.heal(object)
              if(object.life > 0)
                @output += "#{agent.name} => #{object.name}: #{life} + #{healed} => #{object.life}\n"
              else
                @output += "#{agent.name} => #{object.name}: nocauteado\n"
              end
            end
          end
        end
      end
    end
    return @output.chomp
  end
end
