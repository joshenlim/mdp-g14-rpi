import argparse

from src.communicator.utils import fpParser
from src.communicator.utils import pcMsgParser
from src.Logger import Logger

log = Logger()
parser = argparse.ArgumentParser(description='Test communicator utility methods')
parser.add_argument('--verbose', type=bool, const=True, default=None, nargs='?')

def runTests(verbose):
    all_passed = True
    try:
        msg_read = 'EC'
        pc_msg = pcMsgParser(msg_read)
        assert pc_msg['target'] == 'both'
        assert pc_msg['payload']['android'] == 'EC'
        assert pc_msg['payload']['arduino'] == 'EC'
        log.info('pcMsgParser: EC  - Passed!')
    except AssertionError as e:
        all_passed = False
        log.info('pcMsgParser: EC  - Failed!')

    try:
        msg_read = 'ABC'
        pc_msg = pcMsgParser(msg_read)
        assert pc_msg is None
        log.info('pcMsgParser: Unknown Command  - Passed!')
    except AssertionError as e:
        all_passed = False
        log.info('pcMsgParser: Unknown Command  - Failed!')

    try:
        msg_read = 'MDF|ffffffffffffffffffffffffffffdfffbfff7ffefffdfffbffffffffffffffffffffffffffff|00000000000000000000000000000000000000000000000000000000000000000000000000|S|1|1|0|w1'
        pc_msg = pcMsgParser(msg_read)
        assert pc_msg['target'] == 'both'
        assert pc_msg['payload']['android'] == 'MDF|ffffffffffffffffffffffffffffdfffbfff7ffefffdfffbffffffffffffffffffffffffffff|00000000000000000000000000000000000000000000000000000000000000000000000000|S|1|1|0'
        assert pc_msg['payload']['arduino'] == 'w1'
        if verbose:
            log.info('Msg to parse: ' + msg_read)
            log.info('Parsed Android: ' + pc_msg['payload']['android'])
            log.info('Parsed Arduino: ' + pc_msg['payload']['arduino'])
        log.info('pcMsgParser: MDF - Passed!')
    except AssertionError as e:
        all_passed = False
        log.info('pcMsgParser: MDF - Failed!')

    try:
        msg_read = "FP|(1,1,N);(2,1,N);(2,2,E);(2,12,E);(3,12,N);(18,12,N);(18,11,W);(17,11,S)"
        pc_msg = pcMsgParser(msg_read)
        assert pc_msg['target'] == 'both'
        assert pc_msg['payload']['android'] == 'FP|1|1|N|f,tr,tr,tr,tr,tr,tr,tr,tr,tr,tr,tr,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,tl,r'
        assert pc_msg['payload']['arduino'] == 'w1dw9w2aw9w8aw1'
        if verbose:
            log.info('Msg to parse: ' + msg_read)
            log.info('Parsed Android: ' + pc_msg['payload']['android'])
            log.info('Parsed Arduino: ' + pc_msg['payload']['arduino'])
        log.info('pcMsgParser: FP  - Passed!')
    except AssertionError as e:
        all_passed = False
        log.error('pcMsgParser: FP  - Failed!')

    try:
        msg_read = "FP|(1,1,E);(1,5,E);(2,5,N);(4,5,N);(4,6,E);(4,9,E);(5,9,N);(8,9,N);(8,10,E);(8,13,E);(9,13,N);(10,13,N);(10,12,W)"
        pc_msg = pcMsgParser(msg_read)
        assert pc_msg['target'] == 'both'
        assert pc_msg['payload']['arduino'] == 'w4aw3dw4aw4dw4aw2aw1'
        if verbose:
            log.info('Msg to parse: ' + msg_read)
            log.info('Parsed Android: ' + pc_msg['payload']['android'])
            log.info('Parsed Arduino: ' + pc_msg['payload']['arduino'])
        log.info('pcMsgParser: FP2 - Passed!')
    except AssertionError as e:
        all_passed = False
        log.error('pcMsgParser: FP2  - Failed!')

    try:
        msg_read = "FP|(1,1,E);(1,5,E);(2,5,N);(2,4,W)"
        pc_msg = pcMsgParser(msg_read)
        assert pc_msg['target'] == 'both'
        assert pc_msg['payload']['arduino'] == 'w4aw1aw1'
        if verbose:
            log.info('Msg to parse: ' + msg_read)
            log.info('Parsed Android: ' + pc_msg['payload']['android'])
            log.info('Parsed Arduino: ' + pc_msg['payload']['arduino'])
        log.info('pcMsgParser: FP3 - Passed!')
    except AssertionError as e:
        all_passed = False
        log.error('pcMsgParser: FP3  - Failed!')

    if all_passed:
        log.info('All Tests Passed!')

if __name__ == '__main__':
    args = parser.parse_args()
    verbose = args.verbose
    runTests(verbose)
