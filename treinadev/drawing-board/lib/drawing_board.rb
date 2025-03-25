class DrawingBoard
  attr_reader :instructions

  def initialize(instructions)
    @instructions = instructions
  end

  def addEmblem(original, i, j, emblem)
    case emblem
    when "@"
      if(original[i][j] == "*")
        original[i][j] = "%"
      elsif(original[i][j] == "%")
        original[i][j] = "&"
      elsif(original[i][j] == "&")
        original[i][j] = "*"
      else
        original[i][j] = emblem
      end
    when "*"
      if(original[i][j] == "%")
        original[i][j] = "&"
      elsif(original[i][j] == "&")
        original[i][j] = "@"
      elsif(original[i][j] == "@")
        original[i][j] = "%"
      else
        original[i][j] = emblem
      end
    when "%"
      if(original[i][j] == "&")
        original[i][j] = "*"
      elsif(original[i][j] == "@")
        original[i][j] = "&"
      elsif(original[i][j] == "*")
        original[i][j] = "&"
      else
        original[i][j] = emblem
      end
    when "&"
      if(original[i][j] == "%")
        original[i][j] = "*"
      elsif(original[i][j] == "@")
        original[i][j] = "*"
      elsif(original[i][j] == "*")
        original[i][j] = "@"
      else
        original[i][j] = emblem
      end
    end
  end

  def makeArray(original, start, dimensions, emblem)
    x = dimensions[0]
    y = dimensions[1]
    start_x, start_y = start[0], start[1]

    #Corrige o número de linhas
    while original.length < start_x + x do
      original.push(Array.new(original[0].length, ".")) if original[0]
    end

    #Corrige o número de colunas
    original.each do |line|
      while line.length < start_y + y
        line.push(".")
      end
    end

    for i in start_x...(start_x + x) do
      for j in start_y...(start_y + y) do
        addEmblem(original, i, j, emblem)
      end
    end

    return original
  end

  def draw
    new_array = [[]]
    @instructions.each_key do |instruction|
      start = instructions[instruction][:"top_left"]
      dimensions = instructions[instruction][:"dimensions"]
      emblem = instructions[instruction][:"emblem"]

      new_array = makeArray(new_array, start, dimensions, emblem)
    end

    new_array.map { |line| line.join }.join("\n")
  end
end
