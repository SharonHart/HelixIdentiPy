
class Messages:

    START_PRUN = "Pruning regions..."
    END_PRUN = "Pruning completed!"
    FAIL_PRUN = "Pruning failed :("

    START_LINK = "Linking regions..."
    END_LINK = "Linkage completed!"
    FAIL_LINK = "Linking regions failed :("

    START_GRAPH = "Creating graph..."
    END_GRAPH = "Graph ready!"
    FAIL_GRAPH = "Creating graph failed :("


    START_CYL = "Creating an ideal cylinder for your target map..."
    END_CYL = "Your ideal cylinder is ready!"


    START_TEMPLATES = "Generating templates......"
    PROGRESS_TEMPLATES = "Generating templates...... {}%"
    END_TEMPLATES = "Templates ready!"
    FAIL_TEMPLATES = "Generating templates failed :("

    START_CORRELATION = "Correlating......"
    DONE_CORRELATION = "Correlated target with templates!"
    FAIL_CORRELATION = "Correlation failed :("

    START_RUN = "Preparing shotgun to hunt helices..."
    END_RUN = "Done!\tCaught {} helices."

    DONE_TEMPLATES = "Generated {} templates"
    INPUT_FILES_ERROR = "Problem reading input files."
    TEMPLATES_GENERATION_ERROR = "Unable to generate template files."
    CORRELATION_ERROR = "Error correlating Target with template: {}"
    NOT_ENOUGH_ARGS = "Not enough arguments. Please specify <target_map path> <resolution>"
    TEMPLATES_EXIST = "Templates already exist."
    ERROR_READING_TEMPLATE_FILE = "Error reading template file: {}"
    BUMPED_BACK = "Don't be hasty now.. You have some things missing to start this phase, bumping you back for previous phase. \
    This is for your own good."
