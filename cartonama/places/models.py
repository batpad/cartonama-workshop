from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry
try:
    import json
except:
    import simplejson as json

class Feature(models.Model):
    geometry = models.GeometryField(null=True)
    title = models.CharField(max_length=512)

    def get_geojson(self, srid=4326):
#        print srid
        if self.geometry is not None:
            geom = json.loads(self.geometry.transform(srid, True).geojson)
        else:
            geom = {}

        properties = {
            'id': self.id,
            'title': self.title
        }

        return {
            'type': 'Feature',
            'properties': properties,
            'geometry': geom
        }                


    def save_geojson(self, geojson):            
        '''
        pass geojson as dict, not string
        '''
        geojson_geometry_string = json.dumps(geojson['geometry'])        
        geom = GEOSGeometry(geojson_geometry_string)
        properties = geojson['properties']
        #obj = json.loads(geojson)
        title = properties['title']
        self.geometry = geom
        self.title = title
        self.save()
        return self    


# Create your models here.
