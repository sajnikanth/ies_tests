import sys


class Helper():

    @staticmethod
    def get_env():
        env_argument_index = [i for i, arguments in enumerate(sys.argv) if '-env=' in arguments]
        if len(env_argument_index) > 0:
            env = sys.argv[env_argument_index[0]].split('=')[1]
            if env == 'prod':
                return 'production'
            elif env == 'test':
                return 'test'
            else:
                return 'acceptance'
        else:  # Default to acceptance
            return 'acceptance'
