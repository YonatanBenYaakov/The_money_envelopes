from envelope import Envelope
from strategy import ManualStrategy, Automatic_BaseStrategy, N_max_strategy, More_then_N_percent_group_strategy

def cls(): print ("\n" * 20)

envelopes = []
for i in range(100):
    envelopes.append(Envelope())
strategies = []
strategies.append(ManualStrategy(envelopes))                            # user selects manually
strategies.append(Automatic_BaseStrategy(envelopes))                    # random selection
strategies.append(N_max_strategy(envelopes))                            # N-max strategy
strategies.append(More_then_N_percent_group_strategy(envelopes, 0.25))  # N% group strategy


n=-1
while n!=4:
    cls()
    for i in range(len(strategies)):
        print(i, strategies[i].display())
    n = input(f'enter your choice [0-{len(strategies)}]:')
    if n.isdigit():
        n=int(n)
        if n==2:
            N = input(f'enter N max values: ')
            strategies[n].N=int(N)
        elif n==3:
            p = input(f'enter 0-1 number for group size (default=0.25): ')
            try:
                strategies[n].percent = float(p)
            except ValueError:
                print("Invalid input, keeping default percent.")
        if n!=4:    
            strategies[n].play()
        x=input('press any key to continue')
    else:
        pass
