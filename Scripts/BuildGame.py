import subprocess
from datetime import datetime

from . import FileUtils as file_utils
from . import Environment as env

game_name = env.get_env_variable('Game', 'game_name')
builds_dir = env.get_env_variable( "Game", "builds_dir" )

def build_game( log_file ):

    log_file.write( '----------------------------------------------------------------------------------------------------\n' )
    log_file.write( '{} - Step 4: Starting BuildCookRun\n'.format( game_name ) )
    log_file.write( '----------------------------------------------------------------------------------------------------\n' )
    log_file.flush()

    uproject_file = env.get_env_variable( "Game", "uproject_file" )

    ue4_batchfiles_dir = env.get_env_variable( 'Local', "ue4_batchfiles_dir" )
    ue4_binaries_dir = env.get_env_variable( 'Local', "ue4_binaries_dir" )

    result = subprocess.run( [ ue4_batchfiles_dir + 'RunUAT.bat', "BuildCookRun", "-project=" + uproject_file, "-noP4", "-nocompile", "-nocompileeditor", "-installed", "-cook", "-stage", "-archive", "-archivedirectory=" + builds_dir, "-package", "-clientconfig=Development", "-ue4exe=" + ue4_binaries_dir + "UE4Editor-Cmd.exe", "-pak", "-prereqs", "-nodebuginfo", "-targetplatform=Win64", "-build", "-CrashReporter", "-utf8output" ], stdout=log_file )

    log_file.flush()
    return result.returncode == 0

def zip_build():
    latest_build_dir = env.get_env_variable( "Game", "latest_build_dir" )

    now = datetime.now()
    now_str = now.strftime( "%m_%d_%H_%M" )

    file_utils.zip_file_directory( latest_build_dir, builds_dir + game_name + "_" + now_str + ".zip" )
