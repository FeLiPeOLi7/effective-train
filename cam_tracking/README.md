# Rastreamento de Objetos com OpenCV e YOLO

Este projeto realiza o rastreamento de objetos em tempo real usando OpenCV e o modelo YOLOv8. O usuário seleciona manualmente a região de interesse (ROI) no vídeo, e o sistema utiliza um tracker CSRT para seguir o objeto. Caso o tracker perca o alvo, o YOLO é usado para localizar novamente o objeto correto com base na ROI original.

## Funcionalidades

- Seleção manual da ROI inicial.
- Rastreamento do objeto usando `cv.TrackerCSRT_create()`.
- Correção automática com YOLOv8 quando o tracker falha ou a cada N frames.
- Filtro de detecções como confiança mínima.
- Atualização da ROI baseada na melhor correspondência usando IOU.

## Requisitos

- Python
- OpenCV (`opencv-python`)
- Ultralytics YOLO (`ultralytics`)

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/FeLiPeOLi7/effective-train/cam_tracking.git
   cd cam_tracking
   ```
2. Instale as dependências no seu ambiente virtual:
    pip install opencv-python opencv-contrib-python ultralytics

## Uso
1. Rode o script
```bash
python3 tracking.py
```
2. Uma janela será aberta mostrando o vídeo da câmera.

3. Selecione a ROI que deseja rastrear (ENTER após isso).

4. O tracker seguirá o objeto em tempo real. Se perder, o YOLO tentará localizar novamente.

5. Pressione q para sair.

## Melhorias

O projeto ainda sofre com a re-detecção de pessoas e objetos devido as tecnologias usadas, podendo perder o foco e não conseguir encontrar ou perder o foco para um objeto diferente. Além disso, o ROI (Region of Interest) pode mudar de tamanho de vez em quando, por exemplo da face de uma pessoa para todo o seu corpo, devido ao jeito que o YoloV8n é treinado (treinado para detectar pessoas e não faces).
