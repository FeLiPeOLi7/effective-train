import cv2 as cv
from ultralytics import YOLO


def inter_over_union(box1, box2):
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2

    xi1 = max(x1, x2)
    yi1 = max(y1, y2)
    xi2 = min(x1 + w1, x2 + w2)
    yi2 = min(y1 + h1, y2 + h2)

    inter_area = max(0, xi2 - xi1) * max(0, yi2 - yi1)
    box1_area = w1 * h1
    box2_area = w2 * h2
    union = box1_area + box2_area - inter_area

    return inter_area / union if union > 0 else 0


def main():
    # Inicializar o nosso Tracker
    tracker = cv.TrackerCSRT_create()

    # Inicializar YOLO (You Only Look Once) para detectar objetos
    yolo = YOLO("yolov8n.pt")

    # Abrir camera
    cap = cv.VideoCapture(0)  # 0 para a camêra padrão

    if not cap.isOpened():
        print("A câmera não está aberta")
        exit()

    # Ler frame
    ret, frame = cap.read()

    print(f"Ret: {ret} e Fram: {frame}")

    if not ret:
        print("Erro ao ler frame da camera!")
        exit()

    # Escolher ROI (Region of Interest)
    roi = cv.selectROI("tracker", frame)

    tracker.init(frame, roi)

    frame_count = 0
    yolo_refresh_rate = 30
    original_roi = roi

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            print("Erro ao ler o frame")
            break

        frame_count += 1
        
        
        sucess, box = tracker.update(frame)
        
        #Faz um refresh da detecao de objetos com o YOLO
        if not sucess or frame_count % yolo_refresh_rate == 0:
            results = yolo(frame)
           
            best_iou = 0
            best_box = None

            for r in results[0].boxes:
                
                conf = float(r.conf[0].item())
                if conf < 0.6:#Confiaça da detecção maior que 0.6
                    continue

                x1, y1, x2, y2 = r.xyxy[0].tolist()
                candidate_box = (int(x1), int(y1), int(x2 - x1), int(y2 - y1))
                score = inter_over_union(original_roi, candidate_box)

                if score > best_iou:
                    best_iou = score
                    best_box = candidate_box

            if best_box and best_iou > 0.5:
                print(f"Reiniciando tracker com IOU={best_iou:.2f}")
                tracker = cv.TrackerCSRT_create()
                tracker.init(frame, best_box)
                (x, y, w, h) = best_box
                box = best_box
                sucess = True
                cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                original_roi = (x,y,w,h)


        if sucess:
            cv.rectangle(frame, box, (255, 0, 0), 2, 1)
        else:
            print("Falha")

        cv.imshow("Rastreamento do Objeto", frame)

        # Pressione 'q' para sair
        if cv.waitKey(1) & 0xFF == ord("q"):
            break

    # Libera os recursos
    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()
