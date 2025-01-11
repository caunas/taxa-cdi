def exceptionhandler(message: str, status: str, prefix: str = "") -> None:
    status = status.lower()
    
    try:
        if status == "alert":
            cor = "1;33"
            prefixo = f"\033[1;43m{prefix}\033[m: "
        elif status == "error":
            cor = "1;31"
            prefixo = f"\033[1;41m{prefix}\033[m: "
        elif status == "ok":
            cor = "1;32"
            prefixo = f"\033[1;42m{prefix}\033[m: "
    
        if prefix == "":
            prefixo = ""

        print(f"{prefixo}\033[{cor}m{message}\033[m")
    
    except UnboundLocalError as exc:
       print(f"'{status}' isn't a valid status")
    except TypeError as exc:
        print("Invalid ARGS")
    except Exception as exc:
        print(exc)