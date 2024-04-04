

def main(args):
    name = args.get("name", "stranger")
    greeting = "Hello " + name + "!" + " 22"
    b = []
    for i in range(10):
        for j in range(10):
            b.append(i*j)
        if len(b) == 5:
            b = []
    greeting += str(b)
    return {"greeting": greeting}
