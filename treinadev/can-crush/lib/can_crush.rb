class CanCrush
  attr_reader :wall_of_cans, :rocks

  def canWasRocked(can, rock_size)
    if(can - rock_size > 0)
      can = can - rock_size
    else
      can = 0
    end
  end

  def crush(wall_of_cans, rocks)
    result = wall_of_cans

    for i in 0..rocks.length-1 do
      col_smashed = rocks[i][1]
      j=0
      
      while rocks[i][0] > 0 do
        if(result[j][col_smashed] > 0)
          dano = result[j][col_smashed]
          result[j][col_smashed] = canWasRocked(result[j][col_smashed], rocks[i][0])
          rocks[i][0] = rocks[i][0] - dano
          if(rocks[i][0] < 0)
            rocks[i][0] = 0
          end
        else
          if(j < result.length-1)
            j += 1
          else
            break
          end
        end
      end
    end

    return result
  end

  def initialize(wall_of_cans)
    @wall_of_cans = wall_of_cans
  end

  def throw(rocks)
    @rocks = rocks
    crush(@wall_of_cans, rocks)
  end
end
