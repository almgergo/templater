package tmpl_package;

import java.sql.Connection;

import com.loxon.utils.creator.Creatable;
import com.loxon.utils.creator.Creator;
import com.loxon.utils.creator.CreatorContext;

public final class tmpl_classNameHelper implements Creatable {

     public static tmpl_classNameHelper getInstance(final Connection connection) throws Exception
    {
	return (tmpl_classNameHelper) Creator.getSingleton(new CreatorContext(connection), tmpl_classNameHelper.class);
    }

    public void init( final String arg0, final CreatorContext arg1 ) throws Exception {
        // Unused
    }
}