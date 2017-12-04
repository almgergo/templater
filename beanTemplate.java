package tmpl_package;

import java.io.Serializable;

import javax.faces.bean.ManagedBean;
import javax.faces.bean.ViewScoped;

import com.loxon.collection.prodbase.web.utils.JSFUtil;

@ManagedBean
@ViewScoped
public class tmpl_classNameBean implements Serializable {
	
	private static final long serialVersionUID = 1L;

	public static final String BEAN_NAME = JSFUtil.getManagedBeanName(tmpl_classNameBean.class);

}