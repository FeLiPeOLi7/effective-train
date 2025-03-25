class Word
  def longest(phrase)
    maior = 0
    first=0
    maior_palavra = String
    phrase.split() do |word|
      if(first==0)
        maior_palavra = word
        first += 1
      end

      if word.length() >= maior && word.length > 1
        maior = word.length()
        if(word.length == maior_palavra.length)
          for i in 0..word.length()-1
            if(word[i].downcase() < maior_palavra[i].downcase())
              maior_palavra = word
              break
            elsif(word[i].downcase() > maior_palavra[i].downcase())
              break
            end
          end
        else
          maior_palavra = word
        end
      end
    end
    return maior_palavra
  end
  
  def shortest(phrase)
    menor = 0
    menor_palavra = String
    first=0

    phrase.split() do |word|
      if(first==0)
        menor_palavra = word
        menor = menor_palavra.length()
        first += 1
      end

      if word.length() <= menor && word.length > 1
        menor = word.length()
        if(word.length == menor_palavra.length)
          for i in 0..word.length()-1
            if(word[i].downcase() < menor_palavra[i].downcase())
              menor_palavra = word
              break
            elsif(word[i].downcase() > menor_palavra[i].downcase())
              break
            end
          end
        else
          menor_palavra = word
        end
      end
    end
    
    return menor_palavra
  end
end