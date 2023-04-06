import os
from glob import glob
import pydicom as dcm
from tqdm import tqdm
from argparse import ArgumentParser
import pandas as pd


#Todos los tags que sabemos que tienen info confidencial
ETIQUETAS = [
    (0x0008, 0x0022),
    (0x0008, 0x0081),
    (0x0008, 0x0090),
    (0x0008, 0x1050),
    (0x0010, 0x0010),
    (0x0010, 0x0020),
    (0x0010, 0x0030),
    (0x0010, 0x0040),
    (0x0010, 0x1000),
    (0x0010, 0x1010),
    (0x0010, 0x1030),
    (0x0010, 0x2000),
    (0x0010, 0x2110),
    (0x0010, 0x2160),
    (0x0010, 0x2180),
    (0x0010, 0x21b0),
    (0x0010, 0x21c0),
#    (0x0033, 0x1013),
#    (0x0033, 0x1019),
#    (0x0033, 0x101c),
    (0x0038, 0x0300),
]


def main(args):
    # Verificamos que la carpeta existe y tiene contenido
    if os.path.isfile(args.input):
        files = [args.input]
    elif os.path.isdir(args.input):
        files = glob(os.path.join(args.input, "**", "*.dcm"), recursive=True)
    else:
        raise IOError("Archivo ingresado no existe o no contiene DICOM")

    #Creamos la tabla que mantiene los datos:
    outdf = pd.DataFrame(
        columns=["filepath"] + [dcm.datadict.keyword_for_tag(et) for et in ETIQUETAS],
    )

    for file in tqdm(files):
        #abrimos el archivo
        og_ds = dcm.dcmread(file)
        filedf = pd.DataFrame(index=pd.Index([0]))
        filedf["filepath"] = file
        for key in ETIQUETAS:
            try:
                keytext = dcm.datadict.keyword_for_tag(key)
                filedf[keytext] = str(og_ds[key].value)#almacenamos el valor
                del(og_ds[key])
            except ValueError:
                print(f"Campo {keytext} en {file} no fue posible eliminar...")
                continue
            except KeyError:
                print(f"Llave {keytext} no existe, saltando...")
                continue
        
        #print(outdf.head())
        outdf = pd.concat([outdf, filedf], ignore_index=True)
        #Y guardamos el nuevo DICOM
        folderpath, filename = os.path.split(file)
        os.makedirs(os.path.join(args.output, folderpath), exist_ok=True)
        outpath = os.path.join(args.output, file)
        og_ds.save_as(outpath)
        #og_ds.close()

    outdf.to_csv(os.path.join(args.output, "salida.csv"), index=False)



if __name__ == "__main__":
    parser = ArgumentParser(prog="Anonimizador")
    parser.add_argument("input", type=str, help="Ruta donde se encuentran los DICOM")
    parser.add_argument("-o", "--output", default='out/', help="Carpeta de salida")
    args = parser.parse_args()
    main(args)