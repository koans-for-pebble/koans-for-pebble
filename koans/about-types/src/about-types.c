#include <pebble.h>

#define assert(cond, str) (cond ? APP_LOG(APP_LOG_LEVEL_DEBUG, "assertion pass %s", str) :\
                                                                 APP_LOG(APP_LOG_LEVEL_DEBUG, "assertion fail %s", str))

static void run_tests(int a, char b, int c[7], char d[]) {
    psleep(1000);
    APP_LOG(APP_LOG_LEVEL_INFO, "1");
    psleep(1000);
    APP_LOG(APP_LOG_LEVEL_INFO, "2");
    APP_LOG(APP_LOG_LEVEL_DEBUG, "assertion reg about-types-ints");
    APP_LOG(APP_LOG_LEVEL_DEBUG, "assertion reg about-types-chars");
    APP_LOG(APP_LOG_LEVEL_DEBUG, "assertion reg about-types-int-arrays");
    APP_LOG(APP_LOG_LEVEL_DEBUG, "assertion reg about-types-strings");
    assert(a == 592, "about-types-ints");
    assert(b == '@', "about-types-chars");
    bool passed = true;
    for (int i = -3; i < 4; i++) {
        if (c[i + 3] != i) {
            passed = false;
        }
    }
    assert(passed, "about-types-int-arrays");
    assert(strncmp(d, "Meditation", 11) == 0, "about-types-strings");
}

int main(void) {
    /*\
    |*|
    |*| To define a variable (a place to store something), just
    |*|     use `%%type%% %%name%%;`, type being the type of variable
    |*|     you'd like to define (see below) and name being the name
    |*|     you'd like to give the variable.
    |*|
    |*| Assuming you'd like to make a variable of type `count`, which
    |*| doesn't really exist, you'd do the following:
    |*|     -> count a;
    |*|
    |*| You can then set a to something as follows:
    |*|     -> a = 9;
    |*|
    |*| You can combine these to make your code more concise:
    |*|     -> count a = 9;
    |*|
    |*| SOME TYPES OF VARIABLES
    |*|     These aren't all, but they are some of the most foundational.
    |*|
    |*| `int`s store whole numbers from -32,768 to 32,767.
    |*|     -> example: int myNumber = 9001;
    |*|
    |*| `char`s store ASCII characters like 'a', 'r', '3', '#'.
    |*|     You can see a list of ASCII characters at asciitable.com.
    |*|     Use single quotes to assign a value.
    |*|     -> example: char myChar = 'a';
    |*|
    |*| `int[length]` defines an array (list) with length `length`.
    |*|     The length can't be changed after you define the array.
    |*|     -> example: int numbers[2] = {1, 2, 3}; // doesn't work.
    |*|     -> example: int numbers[3] = {1, 2, 3};
    |*|
    |*|     If you leave the length empty, then it will have the length
    |*|     of the data initially used for it.
    |*|
    |*|     -> example: int numbers[] = {1, 1, 2, 3, 5, 8};
    |*|
    |*| `char[length]` is a string (for example, "Hello!").
    |*|     In C, strings are really just arrays of characters, and again,
    |*|     The length can't be changed after you define the array.
    |*|     Because of the way strings work in C, you need to make the
    |*|     string 1 character longer to make space for the NULL character,
    |*|     which signifies the end of a string.
    |*|     -> example: char numbers[3] = "asd"; // won't work
    |*|     -> example: char numbers[4] = "asd"; // works
    |*|
    |*|     If you leave the length empty, then it will have the length
    |*|     of the data initially used for it.
    |*|
    |*|     -> example: char[] sentence = "Hello, World!";
    |*|
    \*/

    /*\
    |*| Your task:
    |*|
    |*| Make an integer `a` set to 592.
    |*| Make a character `b` set to '@'.
    |*| Make an integer array with all natural
    |*|     numbers from -3 to 3 in ascending order.
    |*| Make a string with the text "Meditation"
    |*|
    \*/

    int a = 592;
    char b = '@';
    int c[] = {-3, -2, -1, 0, 1, 2, 3};
    char d[] = "Meditation";

    // Don't worry about the below.
    // By the way, this is a comment.
    // To comment out the rest of a line, just put two slashes.
    /*
    Combining asterisks and slashes makes block commments.
    Block comments span multiple lines.
    */
    /* Even though they don't have to. */

    run_tests(a, b, c, d);
    app_event_loop();
}
