import cv2


# Globals
debug_mode = False
one_cent_radius_in_pixels = 36


def resize_image(image, scale_percent):
    """
    Redimensiona a imagem para altas resoluçes.

    Parameters
    ----------
    image : Matriz
        Imagem a ser redimensionada.
    scale_percent : int
        Valor em porcentagem para a reduçao da imagem.

    Returns
    -------
    Matriz
        Imagem resimensionada
    """
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)

    img = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    return img


def find_circles(image):
    """
    Determina os circulos de uma imagem.

    Parameters
    ----------
    image : Matriz
        Imagem para a procura dos circulos.

    Returns
    -------
    int
        Retorna o raio e a centroide dos circulos detectados.
    """
    # RGB -> GRAY
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Retira os detalhes da imagem
    img_blur = cv2.GaussianBlur(img_gray, (21, 21), cv2.BORDER_CONSTANT)

    '''
        img: imagem em escala de cinza
        CV_HOUGH_GRADIENT: definição do método de detecção
        dp = 1: a razão inversa da resolução sdo acumulador
        min_dist = distância mínima entre centros
        param_1 = 200: limiar máximo para o algoritmo de Canny
        param_2 = 100: limiar para  a detecção dos centros
        min_radius: raio mínimo a ser detectado.
        max_radius: raio máximo a ser detectado.

        circles: vetor com os valores de raio e as coordenadas das centroides
    '''
    circles = cv2.HoughCircles(img_blur, cv2.HOUGH_GRADIENT, 1, 120,
                               param1=53,
                               param2=43,
                               minRadius=50,
                               maxRadius=2000)
    if circles is not None:
        circles = circles
    return circles


def draw_circles(image, coordinates, total, coins):
    """
    Desenha o contorno de circulos, centro, o valor de cada moeda e o valor total em Reais.

    Parameters
    ----------
    image : matrix
        Imagem a ser redimensionada.
    coordinates : list of array
        Coordenadas com o centro dos circulos
    total : float
        Valor total em reais da imagem
    coins : array
        O valor de cada moeda detectadda.
    Returns
    -------
        Figura com os desenhos.
    """
    count = 0
    if debug_mode:
        print("Coins: ", len(coins), "  coordinates: ", len(coordinates[-1]))
    for i in coordinates[0, :]:
        # Circulo
        cv2.circle(image, (i[0], i[1]), i[2], (0, 0, 255), 2)
        # Centro
        cv2.circle(image, (i[0], i[1]), 2, (0, 0, 255), 2)

        if len(coins) == len(coordinates[-1]):
            if debug_mode:
                cv2.putText(image, "R$ " + str(coins[count]) + "  raio:" + str(i[2]),
                            (i[0], i[1]), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 0, 0), 1)
            else:
                cv2.putText(image, "R$ " + str(coins[count]),
                            (i[0], i[1]), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 0, 0), 1)
        count += 1
    cv2.rectangle(image, (0, 55), (150, 20), (255, 255, 255), -1)
    cv2.putText(image, "R$ " + str(total),
                (0, 50), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 0, 0), 1)

    cv2.destroyAllWindows()
    cv2.imshow("Captured Image", image)
    cv2.waitKey(0)


def coins_counter(circle):
    """
    Determina o valor em reais de acordo com  tamanho do circulo.

    Parameters
    ----------
    circle : array
        Valores do raio ou diametro a ser deteminado o valor.

    Returns
    -------
       Retorna o valor total em reais e os valores individuais de cada moeda.
    """

    # Diametro da moeda de 1 centavo em mm - Fonte: Banco central
    brl_rate = 17  # em mm
    # Tolerancia de erro entre o valor aproximado e exato da proporção entre moedas
    tolerance = 0.035

    brl = {
        "1_cent": {
            "value": 0.01,
            "rate": 17 / brl_rate
        },
        "5_cents": {
            "value": 0.05,
            "rate": 22 / brl_rate
        },
        "10_cents": {
            "value": 0.10,
            "rate": 20 / brl_rate
        },
        "25_cents": {
            "value": 0.25,
            "rate": 25 / brl_rate
        },
        "50_cents": {
            "value": 0.50,
            "rate": 23 / brl_rate
        },
        "1_brl": {
            "value": 1,
            "rate": 27 / brl_rate
        },
    }
    # # Seleciona o menor raio - moeda de 1 centavo
    # # min_radius = 27 # em pixels
    # # Obtem as moedas da imagem
    # radius_coins = []
    # radius_coins = [radius[-1] for radius in circle[-1]]
    # # Seleciona o menor raio - moeda de 1 centavo
    min_radius = one_cent_radius_in_pixels

    coins = []
    if debug_mode:
        print("Recebido em coins_counter:", circle)
        for standard_coin in brl:
            print("Referência-> valor: ", brl[standard_coin]['value'], " raio: ", brl[standard_coin]['rate'])
    print('Moedas detectadas:')
    for radius in circle[-1]:
        rate = radius[-1] / min_radius
        for coin in brl:
            value = brl[coin]['rate']
            if (abs(rate - value)) <= tolerance:
                print(brl[coin]['value'])
                coins.append(brl[coin]['value'])
    print("Valor total: R$ {0:.2f}".format(round(sum(coins), 2)))
    return round(sum(coins), 2), coins


def get_image(cam):
    """
    Pega um frame da webcam.

    Parameters
    ----------
    cam : object
        Objeto que referencia a webcam.

    Returns
    -------
        O frame capturado.
    """
    ret, img = cam.read()
    if ret:
        return img
    else:
        print("Imagem não capturada")


def set_webcam(number):
    """
    Inicializa a camera.

    Parameters
    ----------
    number : int
        Numero que a webcam esta associada no computador.

    Returns
    -------
        Objeto que referencia a webcam.
    """
    cam = cv2.VideoCapture(number)
    return cam


'''
    A função realiza operações de acordo com a tecla pressionada
    Se 's': Realiza o processamento
    Se 'q': Finaliza o programa
'''
