class ChessMovements

  def self.readBoard(board)
    piece_details = []

    board.each do |movement|
      movement = movement.split(", ")

      piece = movement[0].split(" ").first
      color = movement[0].split(" ").last
      origin = movement[1].chars
      origin[1] = origin[1].to_i

      details = {:piece => piece, :color => color, :origin => origin, :intention => origin}
      piece_details.push(details)
    end
    return piece_details
  end

  def self.readMovements(piece_movements)
    piece_details = []

    piece_movements.each do |movement|
      movement = movement.split(", ")

      piece = movement[0].split(" ").first
      color = movement[0].split(" ").last
      origin = movement[1].split(" -> ").first.chars
      origin[1] = origin[1].to_i
      intention = movement[1].split(" ").last.chars
      intention[1] = intention[1].to_i

      details = {:piece => piece, :color => color, :origin => origin, :intention => intention}
      piece_details.push(details)
    end
    return piece_details
  end

  def self.kings_move(movement)
    #Movimentos horizontais
    if(((movement[:origin][0].to_i + 1 == movement[:intention][0].to_i) && (movement[:origin][1] == movement[:intention][1])) || ((movement[:origin][0].to_i - 1 == movement[:intention][0].to_i) && (movement[:origin][1] == movement[:intention][1])))
      return "Válido"
    #Movimentos verticais
    elsif(((movement[:origin][1] + 1 == movement[:intention][1]) && (movement[:origin][0] == movement[:intention][0])) || ((movement[:origin][1] - 1 == movement[:intention][1]) && (movement[:origin][0] == movement[:intention][0])))
      return "Válido"
    #Movimentos diagonais  
    elsif(((movement[:origin][0].ord + 1 == movement[:intention][0].ord) && (movement[:origin][1] + 1 == movement[:intention][1])) || ((movement[:origin][0].ord - 1 == movement[:intention][0].ord) && (movement[:origin][1] - 1 == movement[:intention][1])) || ((movement[:origin][0].ord - 1 == movement[:intention][0].ord) && (movement[:origin][1] + 1 == movement[:intention][1])) || ((movement[:origin][0].ord + 1 == movement[:intention][0].ord) && (movement[:origin][1] - 1 == movement[:intention][1])))
      return "Válido"
    else
      return "Inválido"
    end
  end

  def self.valid_movement(piece_movements)
    movements = readMovements(piece_movements)
    valid_movements = []

    movements.each do |movement|
      mov_tower = movement[:origin][0] == movement[:intention][0] || movement[:origin][1] == movement[:intention][1]
      #Diagonal eh onde o x e o y sao iguais
      mov_bishop = (movement[:origin][0].ord - movement[:intention][0].ord).abs == (movement[:origin][1] - movement[:intention][1]).abs
      mov_horse = ((movement[:origin][0].ord - movement[:intention][0].ord).abs == 2 && (movement[:origin][1] - movement[:intention][1]).abs == 1) || ((movement[:origin][0].ord - movement[:intention][0].ord).abs == 1 && (movement[:origin][1] - movement[:intention][1]).abs == 2)

      if(movement[:color] == "branco" || movement[:color] == "branca")
        case movement[:piece]
        when "Peão"
          if(movement[:origin][0] == movement[:intention][0])
            if(movement[:origin][1] + 1 == movement[:intention][1])
              valid_movements << "Válido"
            else
              valid_movements << "Inválido"
            end
          else
            valid_movements << "Inválido"
          end
        when "Torre"
          valid_movements << (mov_tower ? "Válido" : "Inválido")
        when "Bispo"
          valid_movements << (mov_bishop ? "Válido" : "Inválido")
        when "Rei"
          valid_movements << kings_move(movement)
        when "Cavalo"
          valid_movements << (mov_horse ? "Válido" : "Inválido")
        when "Rainha"
          valid_movements << ((mov_bishop || mov_tower) ? "Válido" : "Inválido")
        end
      else
        case movement[:piece]
        when "Peão"
          if(movement[:origin][0] == movement[:intention][0])
            if(movement[:origin][1] - 1 == movement[:intention][1])
              valid_movements << "Válido"
            else
              valid_movements << "Inválido"
            end
          else
            valid_movements << "Inválido"
          end
        when "Torre"
          valid_movements << (mov_tower ? "Válido" : "Inválido")
        when "Bispo"
          valid_movements << (mov_bishop ? "Válido" : "Inválido")
        when "Rei"
          valid_movements << kings_move(movement)
        when "Cavalo"
          valid_movements << (mov_horse ? "Válido" : "Inválido")
        when "Rainha"
          valid_movements << ((mov_bishop || mov_tower) ? "Válido" : "Inválido")
        end
      end
    end

    return valid_movements
  end

  def self.possible_captures(board)
    positions = readBoard(board)
    captures = []
    color_piece = "w"
    color_target = "b"

    positions.each do |piece|
      if(piece[:color] == "branco" || piece[:color] == "branca")
        color_piece = "w"
      else
        color_piece = "b"
      end
      positions.each do |target|
        if(target[:color] == "branco" || target[:color] == "branca")
          color_target = "w"
        else
          color_target = "b"
        end

        if(color_target != color_piece)
          if(piece != target && piece[:piece] != "Peão")#Peão captura diferente
            sample = ["#{piece[:piece]} #{piece[:color]}, #{piece[:origin][0]}#{piece[:origin][1]} -> #{target[:origin][0]}#{target[:origin][1]}"]
            val = valid_movement(sample)
            if(val[0] == "Válido")
              captures << "#{piece[:piece]} #{piece[:color]}, #{piece[:origin][0]}#{piece[:origin][1]} -> #{target[:piece]} #{target[:color]}, #{target[:origin][0]}#{target[:origin][1]}"
            end
          else#Faz a checagem da captura do peão
            if(piece[:origin][0].ord + 1 == target[:origin][0].ord || piece[:origin][0].ord - 1 == target[:origin][0].ord)
              if((piece[:origin][1] + 1 == target[:intention][1] && color_piece == "w") || (piece[:origin][1] - 1 == target[:intention][1] && color_piece == "b"))
                captures << "#{piece[:piece]} #{piece[:color]}, #{piece[:origin][0]}#{piece[:origin][1]} -> #{target[:piece]} #{target[:color]}, #{target[:origin][0]}#{target[:origin][1]}"
              end
            end
          end
        end
      end
    end
    return captures
  end
end