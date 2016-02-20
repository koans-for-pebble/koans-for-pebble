#include <pebble.h>

static void run_tests(int a, int b, int c, int d, int e);

int main(void) {
    /*
     *  These are the numbers you start out with:
     */
    int a = 9;
    int b = 10;
    int c = 11;
    int d = 0;
    int e = 0;

    /*\
    |*|
    |*| In the last koan, you learned all about
    |*|     numbers, characters, arrays and strings.
    |*|
    |*| Time to do something with those numbers.
    |*|
    |*| Here's some operators:
    |*|   + add
    |*|   - subtract
    |*|   * multiply
    |*|   / divide
    |*|
    |*| You can't use floating values (like 2.3).
    |*| In addition, division will result in the result
    |*|     being floored (For example, 9 / 5 is 2.)
    |*|
    |*|
    |*| In addition to writing math like this:
    |*|         c = a + b;  (sets c to the sum of a and b)
    |*| You can also change a's value directly:
    |*|         a += c;     (Increases a by c)
    |*|         b *= 2;     (Doubles the value stored in b)
    |*| There's also a shorter way to write `x += 1;`:
    |*|         x += 1;
    |*|             is equivalent to
    |*|         x++;
    |*|
    \*/

    /*\
    |*|
    |*| Here's what you're supposed to do:
    |*|
    |*| 1. Set `d` to the sum of `b` and `c`. (about-math-addition)
    |*| 3. Set `b` to twice `a`.              (about-math-multiplication)
    |*| 2. Halve `a`.                         (about-math-division)
    |*| 4. Increment `c` by two.              (about-math-increment)
    |*| 5. Decrement `e` by one.              (about-math-decrement)
    |*|
    \*/

    d = b + c;
    b = 2 * a;
    a /= 2;
    c += 2;
    e--;

    // Don't worry about the below.

    run_tests(a, b, c, d, e);
    app_event_loop();
}

#define assert(cond, str) (cond ? APP_LOG(APP_LOG_LEVEL_DEBUG, "assertion pass %s", str) : APP_LOG(APP_LOG_LEVEL_DEBUG, "assertion fail %s", str))

static void run_tests(int a, int b, int c, int d, int e) {
    psleep(1000);
    APP_LOG(APP_LOG_LEVEL_INFO, "1");
    psleep(1000);
    APP_LOG(APP_LOG_LEVEL_INFO, "2");
    APP_LOG(APP_LOG_LEVEL_DEBUG, "assertion reg about-math-addition");
    APP_LOG(APP_LOG_LEVEL_DEBUG, "assertion reg about-math-multiplication");
    APP_LOG(APP_LOG_LEVEL_DEBUG, "assertion reg about-math-division");
    APP_LOG(APP_LOG_LEVEL_DEBUG, "assertion reg about-math-increment");
    APP_LOG(APP_LOG_LEVEL_DEBUG, "assertion reg about-math-decrement");
    assert(a == 4,  "about-math-addition");
    assert(b == 18, "about-math-multiplication");
    assert(c == 13, "about-math-division");
    assert(d == 21, "about-math-increment");
    assert(e == -1, "about-math-decrement");
}
