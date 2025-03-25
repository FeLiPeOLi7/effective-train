class CharacterGenerator
  attr_accessor :characters, :array_of_characters

  def initialize(characters_config)
    @characters = characters_config
    @array_of_characters = []
  end

  def build
    characters.each_key do |character|
      name = character.to_s
      type = characters[:"#{character}"][0]
      strength = characters[:"#{character}"][1]
      max_life = characters[:"#{character}"][2]

      new_character = Character.new(name, type, strength, max_life)

      @array_of_characters << new_character
    end
    return @array_of_characters
  end
end
