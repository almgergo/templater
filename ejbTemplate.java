package tmpl_package;

import javax.ejb.Stateless;
import javax.ejb.TransactionManagement;
import javax.ejb.TransactionManagementType;

import com.loxon.collection.prodbase.ejb.CollectionSessionBeanBase;

@Stateless
@TransactionManagement(TransactionManagementType.BEAN)
public class tmpl_classNameEJB extends CollectionSessionBeanBase implements tmpl_className {

	private static final long serialVersionUID = 1L;

}