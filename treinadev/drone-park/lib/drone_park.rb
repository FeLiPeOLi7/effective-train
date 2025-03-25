class DronePark
  attr_reader :park_map

  def initialize(park_map)
    @park_map = park_map
  end

  def returnFinedPlate(park_matrix, i, j)
  
    placa = ""
    start = j

    while park_matrix[i][start] =~ /[A-Za-z0-9]/ do
      start -= 1
    end

    final = start + 6

    for c in start+1..final do
      placa = placa + park_matrix[i][c]
    end

    return placa
  end

  def returnSideFinedPlate(park_matrix, i, start, final)
  
    placa = ""

    for c in start..final do
      placa = placa + park_matrix[i][c]
    end

    return placa
  end

  def returnAllPlates(park_matrix)

    placas = ""

    park_matrix.each do |line|
      line.each do |char|
        if(char =~ /[A-Za-z0-9]/)
          placas = placas + char
        end
      end
    end

    return placas.scan(/....../).uniq.sort

  end

  def search(symbol)
    park = @park_map.split("\n")
    park_matrix = []
    placas = []
    symbols = []
    i=0
    j=0
  
    park.each do |line|
      park_matrix << line.chars
    end

    park_matrix.each do |line|
      j=0
      line.each do |char|
        if(symbol == char)
          if(j+1 < line.length)
            if(park_matrix[i][j+1] =~ /[A-Za-z0-9]/)
              placas << returnSideFinedPlate(park_matrix, i, j+1, j+6)
            end
          end
          if(j-1 >= 0)
            if(park_matrix[i][j-1] =~ /[A-Za-z0-9]/)
              placas << returnSideFinedPlate(park_matrix, i, j-6, j-1)
            end
          end
          if(i-1 >= 0)
            if(park_matrix[i-1][j] =~ /[A-Za-z0-9]/)
              placas << returnFinedPlate(park_matrix, i-1, j)
            end
          end
          if(i+1 < park_matrix.length)
            if(park_matrix[i+1][j] =~ /[A-Za-z0-9]/)
              placas << returnFinedPlate(park_matrix, i+1, j)
            end
          end
        elsif(symbol == '')
          return returnAllPlates(park_matrix)
        end
        j += 1
      end
      i += 1
    end
  
    return placas.uniq.sort()
  end
end

