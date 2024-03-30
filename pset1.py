# IDENTIFICAÇÃO DO ESTUDANTE:
# Preencha seus dados e leia a declaração de honestidade abaixo. NÃO APAGUE
# nenhuma linha deste comentário de seu código!
#
#    Nome completo: Pedro Henrique Pimentel da Silva
#    Matrícula: 202305389
#    Turma: CC3MB
#    Email: ph024011@gmail.com
#
# DECLARAÇÃO DE HONESTIDADE ACADÊMICA:
# Eu afirmo que o código abaixo foi de minha autoria. Também afirmo que não
# pratiquei nenhuma forma de "cola" ou "plágio" na elaboração do programa,
# e que não violei nenhuma das normas de integridade acadêmica da disciplina.
# Estou ciente de que todo código enviado será verificado automaticamente
# contra plágio e que caso eu tenha praticado qualquer atividade proibida
# conforme as normas da disciplina, estou sujeito à penalidades conforme
# definidas pelo professor da disciplina e/ou instituição.


# Imports permitidos (não utilize nenhum outro import!):
import sys
import math
import base64
import tkinter
from io import BytesIO
from PIL import Image as PILImage


# Classe Imagem:
class Imagem:
    def __init__(self, largura, altura, pixels):
        self.largura = largura
        self.altura = altura
        self.pixels = pixels

    def get_pixel(self, x, y):
        return self.pixels[(y*self.largura) + x]
    
    def get_pixel_fora_limites(self, x, y):
        # Se o valor X for menor que 0 ele vai ser igualado a 0
        if x < 0 : x = 0
        # Se o valor X for maior que a largura ele vai ser igualado ao total da largura menos 1
        #para evitar exceder o valor da largura
        elif x > self.largura - 1: x = self.largura - 1

        if y < 0 : y = 0
        # Se o valor y for maior que a altura ele vai ser igualado ao total da altura menos 1
        #para evitar exceder o valor da largura
        elif y > self.altura - 1 : y = self.altura - 1

        return self.pixels[(y*self.largura) + x]

    def set_pixel(self, x, y, c):
        self.pixels[(y*self.largura) + x] = c

    def aplicar_por_pixel(self, func):
        resultado = Imagem.nova(self.largura, self.altura)
        for x in range(resultado.largura):
            nova_cor = ""
            y = ""
            for y in range(resultado.altura):
                cor = self.get_pixel(x, y)
                nova_cor = func(cor)
                resultado.set_pixel(x, y, nova_cor)
        return resultado

    def aplicar_kernel(self, kernel):
        # Inicializa a lista para guardar os valores resultantes depois da aplicação do kernel
        novos_pixels = []
        # Itera sobre cada pixel na imagem, iniciando da primeira linha e depois
        #passando para as seguintes, seguindo o row-major-order para mexer nos pixels
        for y in range(self.altura):
            for x in range(self.largura):
                # Inicializa a soma para que possa fazer a soma dos kernels
                soma_kernel = 0
                # Itera sobre cada elemento no kernel, da mesma forma que fizemos para y e x,
                #seguindo o row-major-order do kernel
                for kernely in range(len(kernel)):
                    for kernelx in range(len(kernel[0])):
                        # Calcula as coordenadas do pixel do kernel na imagem, onde x e y são, repectivamente,
                        #as coordenadaa atuais do pixel na horizontal e na vertical na imagem original.
                        # O kernelx e kernely são respectivamente o índice horizontal e vertical atual no kernel. 
                        # (len(kernel[0]) // 2)  e (len(kernel) // 2) são usados para descobrir o deslocamento central e
                        #as operações (x + kernelx - len(kernel[0]) // 2) e (y + kernely - len(kernel) // 2) são para 
                        #determinar a localização do pixel na imagem original com base na posição do centro do kernel.
                        pixelx = x + kernelx - len(kernel[0]) // 2
                        pixely = y + kernely - len(kernel) // 2
                        # Obtém o valor do pixel, garantindo que esteja dentro dos limites da imagem
                        pixel = self.get_pixel_fora_limites(pixelx, pixely)
                        # Multiplica o valor do pixel pelo valor correspondente no kernel e acumula dentro do 'soma'
                        soma_kernel += pixel * kernel[kernely][kernelx]
                # Adiciona o valor acumulado do pixel resultante à lista de pixels resultantes e ajusta
                #cada um para não ficar menor que 0 e nem ultrapassar 255
                pixels_resultantes = round(soma_kernel)
                if pixels_resultantes < 0: pixels_resultantes = 0
                elif pixels_resultantes > 255: pixels_resultantes = 255
                novos_pixels.append(pixels_resultantes)
        # Retorna uma nova imagem com os pixels resultantes depois da aplicação do kernel
        return Imagem(self.largura, self.altura, novos_pixels)


    #Usamos a formula  de Lambda c: 255 - c é usado pois quando queremos inverter o
    #valor dos pixels, fazendo que o branco que é 255 vire preto e vice versa, onde o
    #valor c é o pixel atual que sera submetido a operação para a inversão do valor do mesmo.
    def invertida(self):
        return self.aplicar_por_pixel(lambda c: 255 - c)

    def borrada(self, n):
        kernel = []
        for i in range(n):
            # Cria uma lista de zeros com tamanho n para representar uma linha, e essa linha com todos
            #os valores iguais a 0
            linha = [0] * n 
            # Adiciona a linha na matriz do kernel, adicionando até formar a matriz 'n x n'
            kernel.append(linha)

        # Passa por cada pixel da matriz adicionando o valor de 1 / (n**2) que é o valor necessário
        #para que a soma de todos os valores resulte em 1
        for kernely in range(n):
            for kernelx in range(n):
                kernel[kernely][kernelx] = 1 / (n**2)

        return self.aplicar_kernel(kernel)

    def focada(self, n):
        # Cria uma nova imagem com as mesmas dimensões e pixels da imagem original
        imagem_i = Imagem(self.largura, self.altura, self.pixels)

        # Borra a imagem original para usar na formula para obter a imagem nítida
        imagem_borrada = self.borrada(n)

        # Vamos pixel por pixel, aplicando o valor da imagem nítida, pixel por pixel usando a formúla
        #Sx,y = round(2Ix,y - Bx,y-)
        for y in range(self.altura):
            for x in range(self.largura):
                c = 2 * imagem_i.get_pixel_fora_limites(x, y) - imagem_borrada.get_pixel(x,y)
                # Ajusto os pixels para um valor inteiro, positivo que fique entre 0 e 255, mantendo
                pixels = round(c)
                if pixels < 0: pixels = 0
                elif pixels > 255: pixels = 255
                imagem_i.set_pixel(x, y, pixels)

        return imagem_i

    def bordas(self):
        raise NotImplementedError
    


    # Abaixo deste ponto estão utilitários para carregar, salvar e mostrar
    # as imagens, bem como para a realização de testes. Você deve ler as funções
    # abaixo para entendê-las e verificar como funcionam, mas você não deve
    # alterar nada abaixo deste comentário.
    #
    # ATENÇÃO: NÃO ALTERE NADA A PARTIR DESTE PONTO!!! Você pode, no final
    # deste arquivo, acrescentar códigos dentro da condicional
    #
    #                 if __name__ == '__main__'
    #
    # para executar testes e experiências enquanto você estiver executando o
    # arquivo diretamente, mas que não serão executados quando este arquivo
    # for importado pela suíte de teste e avaliação.
    def __eq__(self, other):
        return all(getattr(self, i) == getattr(other, i)
                   for i in ('altura', 'largura', 'pixels'))

    def __repr__(self):
        return "Imagem(%s, %s, %s)" % (self.largura, self.altura, self.pixels)

    @classmethod
    def carregar(cls, nome_arquivo):
        """
        Carrega uma imagem do arquivo fornecido e retorna uma instância dessa
        classe representando essa imagem. Também realiza a conversão para tons
        de cinza.

        Invocado como, por exemplo:
           i = Imagem.carregar('test_images/cat.png')
        """
        with open(nome_arquivo, 'rb') as guia_para_imagem:
            img = PILImage.open(guia_para_imagem)
            img_data = img.getdata()
            if img.mode.startswith('RGB'):
                pixels = [round(.299 * p[0] + .587 * p[1] + .114 * p[2]) for p in img_data]
            elif img.mode == 'LA':
                pixels = [p[0] for p in img_data]
            elif img.mode == 'L':
                pixels = list(img_data)
            else:
                raise ValueError('Modo de imagem não suportado: %r' % img.mode)
            l, a = img.size
            return cls(l, a, pixels)

    @classmethod
    def nova(cls, largura, altura):
        """
        Cria imagens em branco (tudo 0) com a altura e largura fornecidas.

        Invocado como, por exemplo:
            i = Imagem.nova(640, 480)
        """
        return cls(largura, altura, [0 for i in range(largura * altura)])

    def salvar(self, nome_arquivo, modo='PNG'):
        """
        Salva a imagem fornecida no disco ou em um objeto semelhante a um arquivo.
        Se o nome_arquivo for fornecido como uma string, o tipo de arquivo será
        inferido a partir do nome fornecido. Se nome_arquivo for fornecido como
        um objeto semelhante a um arquivo, o tipo de arquivo será determinado
        pelo parâmetro 'modo'.
        """
        saida = PILImage.new(mode='L', size=(self.largura, self.altura))
        saida.putdata(self.pixels)
        if isinstance(nome_arquivo, str):
            saida.save(nome_arquivo)
        else:
            saida.save(nome_arquivo, modo)
        saida.close()

    def gif_data(self):
        """
        Retorna uma string codificada em base 64, contendo a imagem
        fornecida, como uma imagem GIF.

        Função utilitária para tornar show_image um pouco mais limpo.
        """
        buffer = BytesIO()
        self.salvar(buffer, modo='GIF')
        return base64.b64encode(buffer.getvalue())

    def mostrar(self):
        """
        Mostra uma imagem em uma nova janela Tk.
        """
        global WINDOWS_OPENED
        if tk_root is None:
            # Se Tk não foi inicializado corretamente, não faz mais nada.
            return
        WINDOWS_OPENED = True
        toplevel = tkinter.Toplevel()
        # O highlightthickness=0 é um hack para evitar que o redimensionamento da janela
        # dispare outro evento de redimensionamento (causando um loop infinito de
        # redimensionamento). Para maiores informações, ver:
        # https://stackoverflow.com/questions/22838255/tkinter-canvas-resizing-automatically
        tela = tkinter.Canvas(toplevel, height=self.altura,
                              width=self.largura, highlightthickness=0)
        tela.pack()
        tela.img = tkinter.PhotoImage(data=self.gif_data())
        tela.create_image(0, 0, image=tela.img, anchor=tkinter.NW)

        def ao_redimensionar(event):
            # Lida com o redimensionamento da imagem quando a tela é redimensionada.
            # O procedimento é:
            #  * converter para uma imagem PIL
            #  * redimensionar aquela imagem
            #  * obter os dados GIF codificados em base 64 (base64-encoded GIF data)
            #    a partir da imagem redimensionada
            #  * colocar isso em um label tkinter
            #  * mostrar a imagem na tela
            nova_imagem = PILImage.new(mode='L', size=(self.largura, self.altura))
            nova_imagem.putdata(self.pixels)
            nova_imagem = nova_imagem.resize((event.width, event.height), PILImage.NEAREST)
            buffer = BytesIO()
            nova_imagem.save(buffer, 'GIF')
            tela.img = tkinter.PhotoImage(data=base64.b64encode(buffer.getvalue()))
            tela.configure(height=event.height, width=event.width)
            tela.create_image(0, 0, image=tela.img, anchor=tkinter.NW)

        # Por fim, faz o bind da função para que ela seja chamada quando a tela
        # for redimensionada:
        tela.bind('<Configure>', ao_redimensionar)
        toplevel.bind('<Configure>', lambda e: tela.configure(height=e.height, width=e.width))

        # Quando a tela é fechada, o programa deve parar
        toplevel.protocol('WM_DELETE_WINDOW', tk_root.destroy)


# Não altere o comentário abaixo:
# noinspection PyBroadException
try:
    tk_root = tkinter.Tk()
    tk_root.withdraw()
    tcl = tkinter.Tcl()


    def refaz_apos():
        tcl.after(500, refaz_apos)


    tcl.after(500, refaz_apos)
except:
    tk_root = None

WINDOWS_OPENED = False

if __name__ == '__main__':
    """"
    QUESTÃO 2:
    Neste bloco de código, rodamos o filtro de INVERTIDA, onde inverti onde o preto vira branco 
    e vice-versa usando a formula da função 'invertida', assim nós subimos a imagem carregando ela, 
    depois usando o filtro de inversão salvamos a imagem e logo depois usamos a função 'mostrar'
    pra abrirmos o arquivo em uma janela

    i = Imagem.carregar('test_images/bluegill.png')
    invertida = i.invertida()
    invertida.salvar("bluegill_invertido.png")
    invertida.mostrar()

    QUESTÃO 4:
    Neste bloco de código, rodamos a função 'aplicar_kernel', que faz com que um kernelde tamanho
    arbitrário passe por cada pixel da imagem, assim aplicando o kernel em todoso so pixels da imagem.
    Nesse caso a imagem 'pigbird.png' ela alguns pixels a direita e 

    i = Imagem.carregar('test_images/pigbird.png')
    i.salvar("pigbird_sem_kernel.png")
    kernel = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [1, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    imagem_com_kernel = i.aplicar_kernel(kernel)
    imagem_com_kernel.salvar("pigbird_com_kernel.png")
    i.mostrar()
    imagem_com_kernel.mostrar()
    
    i = Imagem.carregar('test_images/cat.png')
    i.salvar("cat_sem_borrar.png")
    i_borrado = i.borrada(5)
    i_borrado.salvar("cat_borrado.png")
    i.mostrar()
    i_borrado.mostrar()
    """

    i = Imagem.carregar('test_images/python.png')
    i.salvar("python_sem_nitidez.png")
    i_nitida = i.focada(11)
    i_nitida.salvar("python_com_nitidez.png")
    i.mostrar()
    i_nitida.mostrar()
    
    pass

    if WINDOWS_OPENED and not sys.flags.interactive:
        tk_root.mainloop()