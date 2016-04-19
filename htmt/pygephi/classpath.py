# adapted http://www.jython.org/jythonbook/en/1.0/appendixB.html#working-with-classpath 
import java
import java.net.URL

import java.lang.reflect.Method
import java.io.File
import java.net.URLClassLoader
import jarray

import java.lang.ClassLoader as javaClassLoader 
from java.net import URLClassLoader 

from java.io import File as javaFile 
from java.net import URL as javaURL 
from java.lang import Object as javaObject 

def addFileorg(path):
    url = java.io.File(path).toURL()
    sysclass = java.net.URLClassLoader
    addURL = sysclass.getDeclaredMethod("addURL", [java.net.URL])
    addURL.setAccessible(True)
    addURL.invoke(java.lang.ClassLoader.getSystemClassLoader(), url)
    return url

#http://www.jython.org/jythonbook/en/1.0/appendixB.html#using-the-classpath-steve-langer
def addFile_try (u):
    parameters = jarray.array([java.net.URL], java.lang.Class)
    sysloader =  java.lang.ClassLoader.getSystemClassLoader()
    sysclass = java.net.URLClassLoader
    method = sysclass.getDeclaredMethod("addURL", parameters)
    a = method.setAccessible(1)
    jar_a = jarray.array([u], java.lang.Object)

    #b = method.invoke(sysloader, jar_a)
    method.invoke(java.lang.ClassLoader.getSystemClassLoader(), jar_a)
    return u


def addFile_nope(u): 
     """Purpose: Call this with u= URL for 
     the new Class/jar to be loaded""" 
     sysloader = javaClassLoader.getSystemClassLoader() 
     sysclass = URLClassLoader 
     method = sysclass.getDeclaredMethod("addURL", [javaURL]) 
     a = method.setAccessible(1) 
     jar_a = jarray.array([u], javaObject) 
     print "YO: "+str(u)
     b = method.invoke(sysloader, [u]) 
     return u 

def addFile(jarFile):
    '''
    http://stackoverflow.com/questions/3015059/jython-classpath-sys-path-and-jdbc-drivers
    import a jar at runtime (needed for JDBC [Class.forName])

    adapted from http://forum.java.sun.com/thread.jspa?threadID=300557
    Author: SG Langer Jan 2007 translated the above Java to Jython
    Author: seansummers@gmail.com simplified and updated for jython-2.5.3b3

    >>> importJar('jars/jtds-1.2.5.jar')
    >>> import java.lang.Class
    >>> java.lang.Class.forName('net.sourceforge.jtds.jdbc.Driver')
    <type 'net.sourceforge.jtds.jdbc.Driver'>
    '''
    from java.net import URL, URLClassLoader
    from java.lang import ClassLoader
    from java.io import File
    m = URLClassLoader.getDeclaredMethod("addURL", [URL])
    m.accessible = 1
    m.invoke(ClassLoader.getSystemClassLoader(), [File(jarFile).toURL()])
    return 


