class SortingChairs
  attr_reader :rules, :chairs, :people

  def fetchPeople(rules)
    rules_book = rules.split("\n")
    people = []

    rules_book.each do |rule|
      if(rule =~ /(.+) senta à esquerda de (.+)/)
        people << $1
        people << $2
      elsif(rule =~ /(.+) senta à direita de (.+)/)
        people << $1
        people << $2
      elsif(rule =~ /(.+) sempre senta no meio/)
        people << $1
      elsif(rule =~ /(.+) não senta no meio/)
        people << $1
      elsif(rule =~ /(.+) não senta ao lado de (.+)/)
        people << $1
        people << $2
      elsif(rule =~ /(.+) sempre senta ao lado de (.+)/)
        people << $1
        people << $2
      end
    end

    return people.uniq
  end

  def initialize(rules)
    @rules = rules
    @chairs = []
    @people = fetchPeople(rules)
  end

  def applyRules
    rules_book = @rules.split("\n")
    selected_chairs = []

    @chairs.each do |possibility|
      is_possible = true
      rules_book.each do |rule|
        #Checar se a regra pra essa pessoa eh vdd
        if(rule =~ /(.+) sempre senta no meio/)
          possibility.each do |seats|
            if(possibility.find_index($1) == 0 || possibility.find_index($1) == possibility.length-1)
              is_possible = false
            end
          end
        elsif(rule =~ /(.+) não senta no meio/)
          possibility.each do |seats|
            if(possibility.find_index($1) != 0 && possibility.find_index($1) != possibility.length-1)
              is_possible = false
            end
          end
        elsif(rule =~ /(.+) senta à esquerda de (.+)/)
          if(possibility.find_index($1) > possibility.find_index($2))
            is_possible = false
          end
        elsif(rule =~ /(.+) senta à direita de (.+)/)
          if(possibility.find_index($1) < possibility.find_index($2))
            is_possible = false
          end
        elsif(rule =~ /(.+) não senta ao lado de (.+)/)
          if(possibility.find_index($1) == possibility.find_index($2) + 1 || possibility.find_index($1) == possibility.find_index($2) - 1)
            is_possible = false
          end
        elsif(rule =~ /(.+) sempre senta ao lado de (.+)/)
          if(possibility.find_index($1) != possibility.find_index($2) + 1 && possibility.find_index($1) != possibility.find_index($2) - 1)
            is_possible = false
          end
        end
      end
      if(is_possible)
        selected_chairs << possibility
      end
    end

    if(selected_chairs.size == 1)
      return selected_chairs.flatten
    elsif(selected_chairs.size == 0)
      return "Impossível aplicar todas as regras"
    else
      return selected_chairs
    end
  end

  def sort
    @chairs = @people.permutation.to_a
    return applyRules
  end
end
