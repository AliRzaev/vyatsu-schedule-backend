package rzaevali.utils;

import java.util.logging.Level;
import java.util.logging.Logger;

public class LogUtils {
    public static Logger getLogger(String name) {
        Logger logger = Logger.getLogger(name);
        logger.setLevel(Level.INFO);
        return logger;
    }
}
