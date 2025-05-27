from Menu import Menyy

def main():
    while True:
        menyy = Menyy()
        menyy.main()

        if not menyy.mynguAlustamisel:
            break
        try:
            menyy.mynguAlustamisel.run()
        except StopIteration:
            continue
        except Exception as e:
            print("Error in game:", e)
            continue

if __name__ == '__main__':
    main()
