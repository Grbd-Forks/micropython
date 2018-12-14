import SCons.Script
from SCons.Environment import Environment
import os
import wget
import zipfile
import platform

EnsureSConsVersion(3, 0, 0)
env = Environment(ENV=os.environ)
#env = Environment(ENV={'PATH': os.environ['PATH']})
env.SetOption('silent', True)

ESP32_IDF_Checkout = "30545f4cccec7460634b656d278782dd7151098e"
ESP32_IDF_URL = "https://github.com/espressif/esp-idf.git"
ESP32_TOOLCHAIN_LINUX64 = "https://dl.espressif.com/dl/xtensa-esp32-elf-linux64-1.22.0-73-ge28a011-5.2.0.tar.gz"
ESP32_TOOLCHAIN_LINUX32 = "https://dl.espressif.com/dl/xtensa-esp32-elf-linux32-1.22.0-73-ge28a011-5.2.0.tar.gz"
ESP32_TOOLCHAIN_WIN32 = "https://dl.espressif.com/dl/xtensa-esp32-elf-win32-1.22.0-73-ge28a011-5.2.0.zip"

ESP8266_SDK = "https://github.com/pfalcon/esp-open-sdk.git"

# https://developer.arm.com/open-source/gnu-toolchain/gnu-rm/downloads
ARM_TOOLCHAIN_WIN32 = "https://developer.arm.com/-/media/Files/downloads/gnu-rm/7-2018q2/gcc-arm-none-eabi-7-2018-q2-update-win32.zip"
ARM_TOOLCHAIN_LINUX64 = "https://developer.arm.com/-/media/Files/downloads/gnu-rm/7-2018q2/gcc-arm-none-eabi-7-2018-q2-update-linux.tar.bz2"

Default(None)
showhelp = True
Help("\nPlease select one of the following options.\n\n")


def nohelpmsg():
    global showhelp
    showhelp = False


def setupopts_venv():
    AddOption('--setup-venvs', dest='setup-venvs', action='store_true', default=False)
    Help("--setup-venvs\t\t\t")
    Help("Setup python virtual environments\n\n")


def setupopts_esp32():
    AddOption('--download-esp32-all', dest='download-esp32-all', action='store_true', default=False)
    Help("--download-esp32-all\t\t")
    Help("Download all related files needed for the ESP32\n")
    AddOption('--download-esp32-idf', dest='download-esp32-idf', action='store_true', default=False)
    Help("--download-esp32-idf\t\t")
    Help("Download just the idf API framework for the ESP32\n")
    AddOption('--download-esp32-toolchain', dest='download-esp32-toolchain', action='store_true', default=False)
    Help("--download-esp32-toolchain\t")
    Help("Download the pre-built toolchain for the ESP32\n\n")


def setupopts_esp8266():
    AddOption('--download-esp8266', dest='download-esp8266', action='store_true', default=False)
    Help("--download-esp8266\t\t")
    Help("Download the sdk files for the esp8266\n")
    AddOption('--build-esp8266', dest='build-esp8266', action='store_true', default=False)
    Help("--build-esp8266\t\t\t")
    Help("Build the sdk files for the esp8266\n\n")


def setupopts_arm():
    AddOption('--download-arm', dest='download-arm', action='store_true', default=False)
    Help("--download-arm\t\t\t")
    Help("Download the precompiled ARM toolchain\n")


def parseopts_venv():
    """Setup Python Vitual Environments"""
    if GetOption('setup-venvs'):
        nohelpmsg()
        env.Execute('tox -c tools/virtenv/tox_dev.ini')


def parseopts_esp32():
    """Download the ESP32 IDF API Libs / toolchain"""
    if GetOption('download-esp32-all') or GetOption('download-esp32-idf'):
        nohelpmsg()
        print("Downloading ESP32-IDF")
        cmdopts = ['git clone ' + ESP32_IDF_URL]
        env.Execute(env.Action(cmdopts, chdir='lib'))
        cmdopts = ['git checkout ' + ESP32_IDF_Checkout]
        env.Execute(env.Action(cmdopts, chdir='lib/esp-idf'))
        cmdopts = ['git submodule update --init']
        env.Execute(env.Action(cmdopts, chdir='lib/esp-idf'))
        print("Finished ESP32 IDF")

    if GetOption('download-esp32-all') or GetOption('download-esp32-toolchain'):
        nohelpmsg()

        if env['PLATFORM'] == "win32":
            print("Windows platform detected")
            print("Downloading ESP32 Toolchain")
            wget.download(ESP32_TOOLCHAIN_WIN32, 'lib/esptoolchain.zip')
            print("\nDecompressing ESP32 Toolchain")
            zip_ref = zipfile.ZipFile('lib/esptoolchain.zip', 'r')
            zip_ref.extractall('lib')
            zip_ref.close()
            os.remove('lib/esptoolchain.zip')

        elif env['PLATFORM'] == "posix":
            print("Posix platform detected")
            downloadurl = ""
            if platform.architecture()[0] == "64bit":
                downloadurl = ESP32_TOOLCHAIN_LINUX64
                print("64bit Posix detected")
            else:
                downloadurl = ESP32_TOOLCHAIN_LINUX32
                print("32bit Posix detected")
            print("Downloading ESP32 Toolchain")
            wget.download(downloadurl, 'lib/esptoolchain.tar.gz')
            print("\nDecompressing ESP32 Toolchain")
            cmdopts = ['tar -xzf esptoolchain.tar.gz']
            env.Execute(env.Action(cmdopts, chdir='lib'))
            os.remove('lib/esptoolchain.tar.gz')
        print("Finished ESP32 Toolchain")


def parseopts_esp8266():
    """Download / Build the ESP8266 SDK"""
    if GetOption('download-esp8266'):
        nohelpmsg()
        print("Downloading ESP8266-SDK")
        cmdopts = ['git clone ' + ESP8266_SDK]
        env.Execute(env.Action(cmdopts, chdir='lib'))
        cmdopts = ['git submodule update --init']
        env.Execute(env.Action(cmdopts, chdir='lib/esp-open-sdk'))
        print("Finished Downloading ESP8266-SDK")

    if GetOption('build-esp8266'):
        nohelpmsg()
        print("Building ESP8266-SDK")
        cmdopts = ['make']
        env.Execute(env.Action(cmdopts, chdir='lib/esp-open-sdk'))
        print("Finished Building ESP8266-SDK")


def parseopts_arm():
    """Download the ARM toolchain"""
    if GetOption('download-arm'):
        nohelpmsg()
        print("Downloading ARM Toolchain")

        if not os.path.exists('lib/gcc-arm-toolchain'):
            os.makedirs('lib/gcc-arm-toolchain')

        if env['PLATFORM'] == "win32":
            print("Windows platform detected - using 32bit precompiled binaries\n")
            wget.download(ARM_TOOLCHAIN_WIN32, 'lib/arm-toolchain.zip')
            print("\nDecompressing ARM Toolchain\n")
            zip_ref = zipfile.ZipFile('lib/arm-toolchain.zip', 'r')
            zip_ref.extractall('lib/gcc-arm-toolchain')
            zip_ref.close()
            os.remove('lib/arm-toolchain.zip')
        else:
            print("Linux platform detected - using 64bit precompiled binaries\n")
            wget.download(ARM_TOOLCHAIN_LINUX64, 'lib/gcc-arm-toolchain/arm-toolchain.tar.bz2')
            print("\nDecompressing ARM Toolchain\n")
            cmdopts = ['tar -xjf arm-toolchain.tar.bz2 --strip 1']
            env.Execute(env.Action(cmdopts, chdir='lib/gcc-arm-toolchain'))
            os.remove('lib/gcc-arm-toolchain/arm-toolchain.tar.bz2')

        print("Finished ARM Toolchain")


setupopts_venv()
setupopts_esp32()
setupopts_esp8266()
setupopts_arm()

parseopts_venv()
parseopts_esp32()
parseopts_esp8266()
parseopts_arm()

if showhelp:
    SetOption("help", True)
