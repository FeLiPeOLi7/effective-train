class TheLastOfUs
  attr_reader :city_map, :paths, :infection_rate

  def returnDistance(x1, y1, x2, y2)
    distance = Math.sqrt(((x2-x1) ** 2) + ((y2-y1) ** 2))
  end

  #Tranforma city_map em um array de hashes para ficar mais fácil de trabalhar
  def readCityMap(city_map)
    locals = []
    
    city_map.split("\n").each do |local|
      base = local.split(":")
      cord = base[1].split(",")
      hash = {:local => base[0], :x => cord[0].to_i, :y => cord[1].to_i}
      locals.push(hash)
    end

    return locals
  end

  #Retorna o valor de contágio do caminho em questão 
  def calculateInfectionOfPath(path, locals, infection_rate)
    path = path.chomp.split(" -> ")
    x_anterior = 0
    y_anterior = 0
    inf_total = 0

    locals.each do |cords|
      if("Base" == cords[:local])
        x_anterior = cords[:x]
        y_anterior = cords[:y]
      end
    end
 
    path.each do |local|
      locals.each do |cords|#Para fazer um match do local e sua coordenada salva em um hash
        if(local == cords[:local])
          distance = returnDistance(x_anterior, y_anterior, cords[:x], cords[:y])
          inf_total = inf_total + infection_rate*distance
          x_anterior = cords[:x]
          y_anterior = cords[:y]
          if(local == "Base")
            inf_total = inf_total / 2
          end
        end
      end
    end
    
    return inf_total
  end

  #Tenta cada caminho, lembrando de qual era a menor infecção
  def tryPaths(paths:, locals:, infection_rate:)
    infection = 0
    lowest_infection = 0
    lowest_path = ""
    first = 1

    paths.each do |path|
      infection = calculateInfectionOfPath(path, locals, infection_rate).round

      if(first != 0)
        lowest_infection = infection
        lowest_path = path
        first = 0
      end

      if(infection < lowest_infection)
        lowest_infection = infection
        lowest_path = path
      end

    end

    hash_of_path = {:path => lowest_path, :infection => lowest_infection}
  end

  def initialize(city_map, paths, infection_rate)
    @city_map = city_map
    @paths = paths.chomp.split("\n")
    @infection_rate = infection_rate
  end

  def infection_monitoring
    locals = readCityMap(city_map)
    hash_result = tryPaths(paths: paths, locals: locals, infection_rate: infection_rate)
    return "O melhor trajeto é #{hash_result[:path]}, com #{hash_result[:infection]} de nível de infecção"
  end
end
