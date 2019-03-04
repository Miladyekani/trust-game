from psychopy import visual, core, monitors, gui, data, event
from psychopy.tools.filetools import fromFile, toFile
import random
import math

debug = 1
exp_params = {'full-screen': not bool(debug),
              'num_trials': 1 if debug else 50,
              }

try:                  # try to get a previous parameters file
    expInfo = fromFile('lastParams.pickle')
except:               # if not there then use a default set
    expInfo = {'participant': 'x', 'width_px': '1920', 'height_px': '1080', 'width_cm': '33',
               'refresh_rate': '60', 'date': data.getDateStr()}

# Present a dialogue to change params
dlg = gui.DlgFromDict(expInfo, title='trust-game', fixed=['date'])
if dlg.OK:
    toFile('data/lastParams.pickle', expInfo)  # save params to file for next time
else:
    core.quit()  # the user hit cancel so exit

file_name = "data/{}-{}.csv".format(expInfo['participant'], expInfo['date'])
scrn = 0
monitor = monitors.Monitor(name='milad', width=int(expInfo['width_cm']), distance=57)
monitor.setSizePix((int(expInfo['width_px']), int(expInfo['height_px'])))
monitor.save()

mywin = visual.Window(monitor=monitor, size=[expInfo['width_px'], expInfo['height_px']], scrn=scrn,
                      fullscr=exp_params['full-screen'], allowGUI=True, units='deg')

# stimuli
letter_height = .5
instr = visual.TextStim(win=mywin, pos=[0, 0], height=letter_height, wrapWidth=10, text="some instructions", )

proposed_amount = 0
respond_txt = visual.TextStim(text="Trusted amount is: ", win=mywin, pos=[0, 2], height=.3, wrapWidth=10)
respond_amnt = visual.TextStim(text="", win=mywin, pos=[0, 0], height=.3, wrapWidth=10)
propose = visual.TextStim(text='How much do you give the other player? ', win=mywin, pos=[0, -1], height=letter_height,
                          wrapWidth=10)
decide = visual.TextStim(text="What do you decide? Press 'f' for trust and 'j' for not trust",
                         win=mywin, pos=[0, -1], height=letter_height, wrapWidth=10)

# make trials
conditions = ['trustee', 'trustor']
stim_set = []
for c in conditions:
    stim_set.append({'role': c, 'amount': math.floor(random.uniform(1, 100))})

trials = data.TrialHandler(stim_set, exp_params['num_trials'], method='random',
                           extraInfo={'subject': expInfo['participant'], 'date': expInfo['date']})
trial_clock = core.Clock()

instr.draw()
mywin.flip()
ready_key = event.waitKeys()
nTrial = 0
for trial in trials:
    respond_amnt.text = trial['amount']
    respond_txt.draw()
    respond_amnt.draw()
    mywin.flip()
    core.wait(3)
    resp = True
    trial_clock.reset()
    decide.draw()
    mywin.flip()
    resp_key = event.waitKeys(timeStamped=trial_clock)
    if resp_key[0][0] == 'f':
        trials.data.add('response', 't')
    elif resp_key[0][0] == 'j':
        trials.data.add('response', 'nt')
    elif resp_key[0][0] == 'escape':
        df = trials.saveAsWideText(file_name)
        mywin.close()
        core.quit()
    event.clearEvents()
    nTrial += 1

mywin.flip()
core.wait(3)

df = trials.saveAsWideText(file_name)
mywin.close()
core.quit()

