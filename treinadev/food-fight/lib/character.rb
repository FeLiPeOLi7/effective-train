class Character
  attr_reader :name, :type, :strength, :max_life
  attr_accessor :life

  def initialize(name, type, strength, max_life)
    @name = name
    @type = type
    @strength = strength
    @max_life = max_life
    @life = max_life
  end

  def life=(damage)
    @life = damage
    if(@life < 0)
      @life = 0
    end

    @life = @life.ceil

    return @life
  end

  def attack(other_character)
    type_strength = 0
    case @type
    when "italiana"
      if(other_character.type == "japonesa")
        other_character.life = other_character.life - (1.5*strength)
        type_strength = 1.5*strength
      elsif(other_character.type == "junina")
        other_character.life = other_character.life - (0.5*strength)
        type_strength = 0.5*strength
      else
        other_character.life = other_character.life - strength
        type_strength = strength
      end
    when "japonesa"
      if(other_character.type == "junina")
        other_character.life = other_character.life - (1.5*strength)
        type_strength = 1.5*strength
      elsif(other_character.type == "italiana")
        other_character.life = other_character.life - (0.5*strength)
        type_strength = 0.5*strength
      else
        other_character.life = other_character.life - strength
        type_strength = strength
      end
    when "junina"
      if(other_character.type == "italiana")
        other_character.life = other_character.life - (1.5*strength)
        type_strength = 1.5*strength
      elsif(other_character.type == "japonesa")
        other_character.life = other_character.life - (0.5*strength)
        type_strength = 0.5*strength
      else
        other_character.life = other_character.life - strength
        type_strength = strength
      end
    end
    return type_strength.floor
  end

  def heal(other_character)
    healed = 0
    if(other_character.life > 0)
      if(other_character.life + strength <= other_character.max_life)
        other_character.life += strength
        healed = strength
      else
        healed = other_character.max_life - other_character.life
        other_character.life = other_character.max_life
      end
    end

    return healed
  end

end

