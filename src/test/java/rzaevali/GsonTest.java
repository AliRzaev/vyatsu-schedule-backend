package rzaevali;

import com.google.common.collect.ImmutableList;
import com.google.gson.Gson;
import org.junit.Test;

import java.util.List;

import static org.junit.Assert.assertEquals;

public class GsonTest {

    @Test
    public void testArrays() {
        List<List<String>> list = ImmutableList.of(
                ImmutableList.of("one", "two"),
                ImmutableList.of("three", "four")
        );

        Gson gson = new Gson();
        String dump = gson.toJson(list);

        List list2 = gson.fromJson(dump, List.class);
        String dump2 = gson.toJson(list2);

        assertEquals(list, list2);
        assertEquals(dump, dump2);
    }
}
