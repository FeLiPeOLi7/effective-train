class MinMax

  def haveRepeatedLetters(array, size)
    for i in 0..size-1 do
      for j in 0..size-1 do
        if(array[i] == array[j] && i != j)
          return true
        end
      end
    end

    return false
  end

  def returnMaxLengthWord(a3)
    word_max_length = (a3.max_by {|x| x.length}).length

    longest_words = a3.select {|x| x.length == word_max_length }

    if longest_words.any? {|x| haveRepeatedLetters(x.chars, x.length)}
      longest_words.find {|x| haveRepeatedLetters(x.chars, x.length)}
    else
      longest_words.first
    end
  end

  def returnMinLengthWord(a3)
    word_min_length = (a3.min_by {|x| x.length}).length

    smallest_words = a3.select {|x| x.length == word_min_length}

    if smallest_words.any? {|x| haveRepeatedLetters(x.chars, x.length)}
      smallest_words.find {|x| haveRepeatedLetters(x.chars, x.length)}
    else
      smallest_words.first
    end
  end

  def find(values)
    a1 = values.split.map
    a2 = []
    a3 = []
    max = 0
    min = 0 

    a1.each do |n|
      if(n.match?(/\A-?\d+\Z/))
        a2 << n.to_i
      else
        a3 << n
      end
    end

    if(a3.empty?)
      max = a2.max
      min = a2.min

      return "Mínimo: #{min}; Máximo: #{max}"
    elsif(a2.empty?)
      max = a3.max_by {|x| x.length}
      min = a3.min_by {|x| x.length}

      return "Mínimo: #{min}; Máximo: #{max}"
    elsif(a3.empty? && a2.empty?)
      return "Vazio"
    end

    longest_word = returnMaxLengthWord(a3)
    smallest_word = returnMinLengthWord(a3)

    if(a2.max > longest_word.length)
      max = a2.max
    elsif(a2.max == longest_word.length)
      if(haveRepeatedLetters(longest_word.chars, longest_word.length))
        max = longest_word 
      else
        max = a2.max
      end
    else
      max = longest_word
    end

    if(a2.min < smallest_word.length)
      min = a2.min
    elsif(a2.min == smallest_word.length)
      if(haveRepeatedLetters(smallest_word.chars, smallest_word.length))
        min = smallest_word 
      else
        min = a2.min
      end
    else
      min = smallest_word
    end
    
    return "Mínimo: #{min}; Máximo: #{max}"
  end
end