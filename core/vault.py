from pathlib import Path
from config import Config
from core.metadata import MetaStore
from utils.file_utils import ensure_dir, prompt_yes_no, copy_file

def init_vault(cfg: Config) -> MetaStore:
    """
    Ensure vault directory exists and return metadata store.
    """
    ensure_dir(cfg.vault_dir)
    return MetaStore(cfg.db_path)

def add_file(cfg: Config, meta: MetaStore, src: Path) -> None:
    """
    Copy a file into the vault and update metadata.
    """

    #checks if the source really exists, or if this path is a regular file 
    # if not return this as error and turn into string source  
    if not src.exists() or not src.is_file():
        raise FileNotFoundError(str(src))


    dst = cfg.vault_dir/ src.name
    overwrite = True
    if dst.exists():
        #if the destination exists we get prompted to yes or no
        overwrite = prompt_yes_no(f"File{src.name} already exisits in vault.Overwrite ?")
        #if the person chooses not to overwrite it we just return
        if not overwrite:
            return 
    
    #this will copy the file and update the metadata that we have 
    copy_file(src,dst)
    meta.upsert(dst.name,dst.stat().st_size)



def paste_files(cfg: Config, filenames: list[str], cwd: Path) -> list[str]:
    """
    Copy selected vault files into cwd.
    """
    #create a list of string
    pasted = []
    #loop through filenames list which im geussing it our list
    for name in filenames:
        #tries copying the files from the vault to the cwd
        src = cfg.vault_dir / name
        #if does not exist check and moves to next one 
        if not src.exists() or not src.is_file():
            continue
    
        #constructs the destinaiton path, "/" is a way to join paths in pathlib, so anme is being joined to cwd
        dst = cwd/ name
        overwrite = True
        #if already a destination asks user to overwrite
        if dst.exists():
            overwrite = prompt_yes_no(f"File{name} already exists in cwd.Overwrite?")
        if not overwrite:
            continue

        copy_file(src,dst)
        #add the files into the list and return it,keeps trackof what files been pasted
        pasted.append(name)
    
    #return the list of pasted files
    return pasted
        
        
