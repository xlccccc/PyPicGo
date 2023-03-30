import argparse

from pypicgo.core.config import Settings
from pypicgo.core.execute import create_uploader
from pypicgo.core.logger import logger
from pypicgo.core.base.plugin import BeforePlugin, AfterPlugin, FinallyPlugin

def action():

    parser = argparse.ArgumentParser(
        prog='PyPicGo',
        add_help=True, 
        description='Welcom to PyPicGo'
        )
    parser.add_argument('-n', '--name', type=str, help="uploader name", metavar="github")
    # Aparser.add_argument('-f', '--files', nargs='+', required=True, type=str, help="upload files list", metavar="./img.png")
    parser.add_argument('-m', '--mdfiles')
    args = parser.parse_args()
    uploader_name = args.name
    markdown_file = args.mdfiles
    mdFileRead1 = open(markdown_file, 'r', encoding='utf-8')
    mdFileReadText = mdFileRead1.readlines()
    mdFileRead1.close()
    mdFileRead2 = open(markdown_file, 'r', encoding='utf-8')
    mdFileWriteText = mdFileRead2.read()
    mdFileRead2.close()
    files = mdFileFindImg(mdFileReadText)
    settings = Settings(uploader_name=uploader_name)
    uploader = settings.uploader_class
    uploader_config = settings.uploader_config
    plugins = settings.plugins
    with create_uploader(uploader, uploader_config, plugins) as uploader:
        logger.info('upload start')
        for filepath in files:
            logger.info(f'upload file [{filepath}]')
        
            uploader.do(filepath)
        f = open('url.txt', 'r')
        newFilePaths = f.readlines()
        for filepath, newfilepath in zip(files, newFilePaths):
            mdFileWriteText = mdFileChange(mdFileWriteText, filepath, newfilepath)
        mdFileWrite = open(markdown_file, 'w', encoding='utf-8')
        mdFileWrite.write(mdFileWriteText)
        mdFileWrite.close()
        logger.info('all file has been handled')

def mdFileFindImg(mdFile):
    files = []
    for line in mdFile:
        if line.find('![image-') != -1:
            start = line.find('(')
            end = line.find(')', start)
            files.append(line[start+1:end])
    return files



def mdFileChange(mdFile, oldFilepath, newFilepath):
    if mdFile.find(oldFilepath) != -1:
        potision = mdFile.find(oldFilepath)
        start = mdFile.find('![image-', potision - 30, potision)
        end  = mdFile.find(')', potision)     
        mdFile = mdFile.replace(mdFile[start:end + 1], '![](' + newFilepath + ')')
    return mdFile

if __name__ == '__main__':
    action()
